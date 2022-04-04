from datetime import date, timedelta
import json
from pprint import pprint
from typing import List, Dict, Any
import random
from ltt.add_attributes import _add_new_attribute
from ltt.db_connections import sql_query, sql_command


def add_fake_attributes():
    # Get attribute types
    result = sql_query("SELECT attribute_type FROM register.attribute_types;")
    attribute_types = [row[0] for row in result]

    # Get properties
    result = sql_query("SELECT wra_property_id FROM register.properties;")
    property_ids = [row[0] for row in result]

    # Loop through the properties and create some fictional attributes
    for prop_id in property_ids:
        if prop_id < 4:
            continue

        # Sample a number of attributes (from 0 to 4)
        attributes = _sample_attributes(attribute_types)

        # For each attribute
        for attribute in attributes:
            # Determine the attribute details
            kwargs = _determine_kwargs(attribute)
            pprint(kwargs)
            # Add to database
            _add_new_attribute(wra_property_id=prop_id, **kwargs)


def _sample_attributes(attribute_types: List[str]) -> List[str]:
    n_attributes = random.randint(0, 4)
    attributes = random.sample(attribute_types, n_attributes)
    if "second_home" in attributes and "buy_to_let" in attributes:
        attributes.remove("second_home")
    return attributes


def _determine_kwargs(attribute: str) -> Dict[str, Any]:
    if attribute == "second_home":
        kwargs = _determine_second_home_kwargs()
    elif attribute == "buy_to_let":
        kwargs = _determine_buy_to_let_kwargs()
    elif attribute == "attribute_a":
        kwargs = _determine_attribute_a_kwargs()
    elif attribute == "attribute_b":
        kwargs = _determine_attribute_b_kwargs()
    else:
        kwargs = {}

    return kwargs


def _determine_second_home_kwargs() -> Dict[str, Any]:
    kwargs = {
        "attribute_type": "second_home",
        "bool_value": True,
        "valid_from": _generate_date_in_past(),
    }
    return kwargs


def _determine_buy_to_let_kwargs() -> Dict[str, Any]:
    kwargs = {
        "attribute_type": "buy_to_let",
        "bool_value": True,
        "valid_from": _generate_date_in_past(),
    }
    return kwargs


def _determine_attribute_a_kwargs() -> Dict[str, Any]:
    kwargs = {
        "attribute_type": "attribute_a",
        "numeric_value": random.randint(1, 2),
        "valid_from": _generate_date_in_past(),
    }
    return kwargs


def _determine_attribute_b_kwargs() -> Dict[str, Any]:
    kwargs = {
        "attribute_type": "attribute_b",
        "numeric_value": random.randint(1, 3),
        "valid_from": _generate_date_in_past(),
    }
    return kwargs


def _generate_date_in_past() -> str:
    today = date.today()
    delta = timedelta(days=random.randint(0, 6000))
    return str(today - delta)


def generate_address():
    number = random.randint(1, 200)
    street = random.choice([
        "England Street",
        "England Lane",
        "England Drive"
    ])
    return f"{number}, {street}, Upper Leadworth"


def insert_property(address):
   sql_command(f"""
            INSERT INTO register.properties(address) VALUES
                ('{address}');
        """)
   wra_property_id = sql_query(f"""
                SELECT wra_property_id
                FROM register.properties
                WHERE address = '{address}';
           """)
   return wra_property_id[0][0]


def insert_point(wra_property_id, feature):
    uprn = feature["properties"]["UPRN"]

    geometry = feature["geometry"]
    geom_text = f"{geometry['type'].upper()}({geometry['coordinates'][0]} {geometry['coordinates'][1]})"
    
    command = (f"""
                INSERT INTO register.points(uprn, wra_property_id, geom) VALUES
                    ({uprn}, {wra_property_id}, ST_GeomFromText('{geom_text}', 27700));
            """)
    print(command)
    sql_command(command)


def add_english_uprns():
    with open("../LTT_calculation/fiction/English_UPRN.geojson", "r") as f:
        j = json.load(f)
    
    features = j["features"]
    addresses = []
    while len(addresses) < 64:
        address = generate_address()
        if address not in addresses:
            addresses.append(address)
    
    for feature, address in zip(features, addresses):
        wra_property_id = insert_property(address)
        insert_point(wra_property_id, feature)
    
