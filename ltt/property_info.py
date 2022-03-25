"""
Functions for gathering info about a property.

Intended to sit behind the /property_info API
"""

from ltt.db_connections import sql_query
from ltt.data_object_models import Attribute


def get_property_info(wra_property_id: int):
    result = sql_query(
        f"""
        SELECT *
        FROM register.attributes
        JOIN register.properties USING(wra_property_id)
        WHERE wra_property_id = {wra_property_id}
        AND CURRENT_DATE BETWEEN valid_from AND valid_to;
    """
    )
    if not result:
        return

    property_info = {
        "wra_property_id": wra_property_id,
        "address": result[0][8],
        "attributes": {},
    }

    for row in result:
        attribute = Attribute(
            wra_attribute_id=row[0],
            wra_property_id=row[1],
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