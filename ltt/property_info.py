"""
Functions for gathering info about a property.

Intended to sit behind the /property_info API
"""

from typing import Optional, Dict, Any
from ltt.db_connections import sql_query
from ltt.data_object_models import Attribute


def get_property_info(
    platform_property_id: Optional[int] = None, address: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Retruns information and attrributes related to the property

    Parameters:
        - platform_property_id: the internal (to the platform) unique identifier
          for the property.
        - address: the property address, exactly as it appears in the database

    Returns:
        - property_info dictionaty, with both property identifiers 
          (platform_property_id and address) and nested attributes linked to that 
          property.
    """
    if platform_property_id:
        return _get_property_info_from_id(platform_property_id)

    if address:
        return _get_property_info_from_address(address)

    raise AttributeError(
        "one from platform_property_id or address must be provided"
    )


def _get_property_info_from_id(
    platform_property_id: int,
) -> Optional[Dict[str, Any]]:
    result = sql_query(
        f"""
        SELECT *
        FROM register.attributes
        JOIN register.properties USING(platform_property_id)
        WHERE platform_property_id = {platform_property_id}
        AND CURRENT_DATE BETWEEN valid_from AND valid_to;
    """
    )
    if not result:
        return

    property_info = {
        "platform_property_id": platform_property_id,
        "address": result[0][8],
        "attributes": {},
    }

    for row in result:
        attribute = Attribute(
            platform_attribute_id=row[0],
            platform_property_id=row[1],
            attribute_type=row[2],
            bool_value=row[3],
            text_value=row[4],
            numeric_value=float(row[5]) if row[5] else None,
            valid_from=str(row[6]),
            valid_to=str(row[7]),
        )
        property_info["attributes"].update(
            {attribute.attribute_type: attribute.value}
        )

    return property_info


def _get_property_info_from_address(address: str) -> Optional[Dict[str, Any]]:
    result = sql_query(
        f"""
        SELECT *
        FROM register.attributes
        JOIN register.properties USING(platform_property_id)
        WHERE address = '{address}'
        AND CURRENT_DATE BETWEEN valid_from AND valid_to;
    """
    )
    if not result:
        return

    property_info = {
        "platform_property_id": result[0][0],
        "address": address,
        "attributes": {},
    }

    for row in result:
        attribute = Attribute(
            platform_attribute_id=row[0],
            platform_property_id=row[1],
            attribute_type=row[2],
            bool_value=row[3],
            text_value=row[4],
            numeric_value=float(row[5]) if row[5] else None,
            valid_from=str(row[6]),
            valid_to=str(row[7]),
        )
        property_info["attributes"].update(
            {attribute.attribute_type: attribute.value}
        )

    return property_info

