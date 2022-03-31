"""
Localised LTT calclulator
"""

from typing import Dict, Optional, Union
from ltt.db_connections import sql_query
from ltt.data_object_models import Attributes


SCHEDULES = [
    "rates_main_residential",
    "rates_higher_residential",
    "rates_higher_plus_residential",
]
SCHEDULE_ATTRIBUTES = ["second_home", "buy_to_let"]


def calculate_tax(
    address: str,
    value: int,
    attributes: Optional[Attributes],
    use_polygon: bool = False,
) -> float:
    """
    Calculates localised land transaction tax.

    Parameter:
        - address: the address of the property written as exact string, no
          address parser is used.
        - value: the property value against which to calculate tax
        - attributes: dictionary of declarative attributes which have
          associated tax rules in "attribute", "value" format. All available
          attributed are in the attribute_rules table, are listed below and
          can be grouped into 3 strategies (that could have more attributes
          added at a later date (behavior when there are multiple attributes
          in the same strategy are not yet implemented):

          Schedule determining attributes:
          --------------------------------
          These are attributes which, if present, determine what minimum
          schedule must be applied (note: in this implementation, schedules
          must be ranked and the attributes below will bump the property up to
          higher schedules with the rates_main_residential as the defult).

            * second_home
            * buy-to-let

          These attributes should be written exactly ad above and assigned a
          value of True if present. If not present, do not declare them
          (the function currently doesn't handle False values).

          The initial tax will be set based off these attributes first before
          assessing the other types below.

          Tax multiplying attributes:
          ---------------------------

          These will multiply the base tax.

            * attribute_a

          Fixed tax addition attributes:
          ------------------------------
          These will add a fixed amount onto the tax, based on the value.

            * attribute_b

    Returns:
        - tax, rounded to nearest penny
    """
    # Determine schedule
    schedule = _determine_schedule(attributes) if attributes else SCHEDULES[0]

    # Determine tax zone and apply rate
    if use_polygon:
        tax_zones = tax_zone_lookup_polygon(address)
    else:
        tax_zones = tax_zone_lookup(address)

    tax = _apply_schedule(schedule, tax_zones, value)

    # Modify rate based on attributed declared
    if attributes:
        for attribute, attr_value in attributes:
            if attribute not in SCHEDULE_ATTRIBUTES:
                tax = _modify_rate(tax, attribute, attr_value)

    # Round to nearest penny and return
    tax = round(tax, 2)
    return tax


def _determine_schedule(
    attributes: Attributes,
) -> str:
    """Returns the schedule (by table name) to be used."""
    # Set the default schedule index as 0 (corresponds to
    # rates_main_residential)
    schedule_idx = 0

    # Loop through the attributes which are relevant to schedule assignment
    for attribute, atr_value in attributes:
        if attribute in SCHEDULE_ATTRIBUTES and atr_value is True:

            # Check the minimum schedule for a property with that attribute
            # and update if higher that the current assigned schedule index
            # Note: atr_value must be int as this is how it is stored in
            # attribute_rules table so it can share with other attribute
            # modification values.
            min_schedule_idx = _min_schedule_idx(attribute, int(atr_value))
            if min_schedule_idx > schedule_idx:
                schedule_idx = min_schedule_idx

    return SCHEDULES[schedule_idx]


def _min_schedule_idx(attribute: str, atr_value: int) -> int:
    """
    Returns the minimum schedule to be applied if the given attribute is
    True in terms of the index of SCHEDULES.
    """
    query = f"""
        SELECT modification_value
        FROM attribute_rules
        WHERE attribute = '{attribute}' AND attribute_value = '{atr_value}';
    """
    result = sql_query(query)
    min_schedule_idx = int(result[0][0])

    return min_schedule_idx


def _apply_schedule(
    schedule: str, tax_zones: Dict[str, float], value: float
) -> float:
    """
    Returns the tax (before modifiers applied) from schedule.

    Method if tax split accross multiple zones:
        * Calculate tax for 100% of value accross each tax zone
        * Multiply by proportion in each tax zone
        Note: must split by tax zone after otherwise incorrect tax will be
        allocated.
    """
    tax = 0.0
    for tax_zone, proportion in tax_zones.items():
        local_tax = _apply_schedule_single_tax_zone(schedule, tax_zone, value)
        tax += local_tax * round(proportion, 2)

    return tax


def _apply_schedule_single_tax_zone(
    schedule: str, tax_zone: str, value: float
) -> float:
    """Returns tax based of single tax zone"""
    query = f"""
        SELECT lower_bound, upper_bound, {tax_zone}
        FROM {schedule}
        WHERE lower_bound < {value};
    """
    result = sql_query(query)
    tax = 0
    for band in result:
        lower, upper, rate = band
        if value > upper:
            full_band = upper - lower
            tax += full_band * float(rate)
        else:
            value_in_band = value - lower
            tax += value_in_band * float(rate)

    return tax


def _modify_rate(
    tax: float, attribute: str, atr_value: Union[int, float, bool, str]
) -> float:
    """Returns modified tax based on value of attribute"""
    if atr_value is None:
        return tax
    # Get method and value
    query = f"""
        SELECT method, modification_value
        FROM attribute_rules
        WHERE attribute = '{attribute}' AND attribute_value = '{atr_value}';
    """
    result = sql_query(query)
    method, modification_value = result[0]
    modification_value = float(modification_value)

    # Apply method and value
    if method == "multiply":
        tax *= 1 + modification_value
    elif method == "add":
        tax += modification_value

    return tax


def tax_zone_lookup(address: str) -> Dict[str, float]:
    """
    Returns tax zone for a given address which is associated with a point uprn
    location (difference implementation required for polygon address
    representation).

    Parameters:
        - address: The address to lookup. Must be exaxtly as it appears in the
          uprn_address table, case and whitespace sensitive. No address parser
          is implemented.

    Returns:
        - tax_zone: the tax zone that the address is in written like
          "north tax zone" - can be changed to zone ID later.
    """
    query = f"""
        SELECT tax_zone 
        FROM uprn_address
        JOIN uprn_location USING(uprn)
        JOIN tax_zones 
            ON ST_Contains(tax_zones.wkb_geometry, uprn_location.wkb_geometry)
        WHERE uprn_address.address = '{address}';
    """
    result = sql_query(query)

    # result will be single string in tuple in list so need to extract
    if result:
        tax_zone = result[0][0]
    else:
        raise AttributeError("Address not in database")

    return {tax_zone: 1.0}


def tax_zone_lookup_polygon(address: str) -> Dict[str, float]:
    """
    Returns a dictionary with proprtion of land in each tax_zone for a given
    address which is associated with a polygon land area.

    Parameters:
        - address: The address to lookup. Must be exaxtly as it appears in the
          uprn_address table, case and whitespace sensitive. No address parser
          is implemented.

    Returns:
        - tax_zone_proportions: Dictionary of with key: value as
        tax_zone: proportion of land polygon within

    """
    query = f"""
        SELECT
            land_address.land_address AS property_address
          , tax_zones.tax_zone AS tax_zone
          , ST_Area(ST_Intersection(land_address.wkb_geometry, tax_zones.wkb_geometry)) 
            / total_areas.total_area AS proportions_in_zone
        FROM land_address
        JOIN tax_zones ON ST_Intersects(land_address.wkb_geometry, tax_zones.wkb_geometry)
        JOIN (
            SELECT
                land_address
              , ST_Area(wkb_geometry) AS total_area
              FROM land_address
        ) AS total_areas ON land_address.land_address = total_areas.land_address
        WHERE land_address.land_address = '{address}';
    """
    result = sql_query(query)

    if result:
        tax_zone_proportions = {}
        for row in result:
            tax_zone_proportions.update({row[1]: row[2]})
    else:
        raise AttributeError("Address not in database")

    return tax_zone_proportions
