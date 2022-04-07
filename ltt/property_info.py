"""
Functions for gathering info about a property.

Intended to sit behind the /property_info API
"""

import json
from typing import Optional, Dict, Any
from ltt.db_connections import sql_query
from ltt.data_object_models import Attribute


def get_property_info(
    platform_property_id: Optional[int] = None,
    address: Optional[str] = None,
    privacy_level: int = 2,
) -> Optional[Dict[str, Any]]:
    """
    Retruns information and attrributes related to the property

    Parameters:
        - platform_property_id: the internal (to the platform) unique identifier
          for the property.
        - address: the property address, exactly as it appears in the database
        - privacy_level: determines which privacy level attributes will be
          returned.

    Returns:
        - property_info dictionaty, with both property identifiers
          (platform_property_id and address) and nested attributes linked to that
          property.
    """

    if platform_property_id:
        result = _id_query(platform_property_id, privacy_level)
    elif address:
        result = _address_query(address, privacy_level)
    else:
        raise AttributeError(
            "one from platform_property_id or address must be provided"
        )

    if not result:
        return

    # Create return dictionary
    property_info = {
        "identifiers": {
            "uprn": result[0][6],
            "platform_property_id": result[0][0],
            "address": result[0][5],
        },
        "attributes": {},
        "geospatial": {},
    }

    # Add geojsons seperately and handle empty values
    # Note: Better solution would be to not add the field into the dictionary
    # if there is no result (rather than add "not in database") to keep the
    # field value types consistent but this will look more seld explanatory
    # for early PoC demos
    if result[0][7]:
        uprn_point_location = json.loads(result[0][7])
    else:
        uprn_point_location = "not in database"

    if result[0][8]:
        extent = json.loads(result[0][8])
    else:
        extent = "not in database"

    property_info["geospatial"].update(
        {"uprn_point_location": uprn_point_location}
    )
    if privacy_level > 1:
        property_info["geospatial"].update({"extent": extent})

    # Add attributes
    for row in result:
        attribute = Attribute(
            platform_property_id=row[0],
            attribute_type=row[1],
            bool_value=row[2],
            text_value=row[3],
            numeric_value=float(row[4]) if row[4] else None,
        )
        property_info["attributes"].update(
            {attribute.attribute_type: attribute.value}
        )

    return property_info


def _id_query(platform_property_id: int, privacy_level: int = 2):
    return sql_query(
        f"""
        SELECT
            platform_property_id
          , attribute_type
          , bool_value
          , text_value
          , numeric_value
          , address
          , uprn
          , ST_AsGeoJSON(register.points.geom) AS uprn_point_location
          , ST_AsGeoJSON(register.polygons.geom) AS extent
        FROM register.attributes
        JOIN register.properties USING(platform_property_id)
        LEFT JOIN register.points USING(platform_property_id)
        LEFT JOIN register.polygons USING(platform_property_id)
        JOIN register.attribute_types USING(attribute_type)
        WHERE platform_property_id = {platform_property_id}
        AND privacy_level <= {privacy_level}
        AND CURRENT_DATE BETWEEN valid_from AND valid_to;
    """
    )


def _address_query(address: str, privacy_level: int = 2):
    return sql_query(
        f"""
        SELECT
            platform_property_id
          , attribute_type
          , bool_value
          , text_value
          , numeric_value
          , address
          , uprn
          , ST_AsGeoJSON(register.points.geom) AS uprn_point_location
          , ST_AsGeoJSON(register.polygons.geom) AS extent
        FROM register.attributes
        JOIN register.properties USING(platform_property_id)
        LEFT JOIN register.points USING(platform_property_id)
        LEFT JOIN register.polygons USING(platform_property_id)
        JOIN register.attribute_types USING(attribute_type)
        WHERE address = '{address}'
        AND privacy_level <= {privacy_level}
        AND CURRENT_DATE BETWEEN valid_from AND valid_to;
    """
    )
