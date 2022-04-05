import datetime
from typing import Optional, Union
from ltt.db_connections import sql_query, sql_command
from ltt.data_object_models import Attribute


def add_attribute(
    platform_property_id: int,
    attribute_type: str,
    bool_value: Optional[bool] = None,
    text_value: Optional[str] = None,
    numeric_value: Optional[Union[int, float]] = None,
    valid_from: Optional[str] = str(datetime.date.today()),
    valid_to: Optional[str] = None,
    debug: Optional[bool] = False,
):
    attribute = Attribute(
        platform_property_id=platform_property_id,
        attribute_type=attribute_type,
        bool_value=bool_value,
        text_value=text_value,
        numeric_value=numeric_value,
        valid_from=valid_from,
        valid_to=valid_to,
    )
    _add_attribute(attribute, debug=debug)


def _add_attribute(attribute: Attribute, debug: Optional[bool] = False):
    if _attribute_type_exists(attribute.attribute_type):
        existing_attribute = _get_attribute(attribute)

        # If attribute exists and values are the same, change nothing but
        # inform user
        if existing_attribute:
            if (
                attribute.attribute_type == existing_attribute.attribute_type
                and attribute.value == existing_attribute.value
            ):
                print(
                    "Attribute for property already exists. No records changed"
                )
                return

            # If value is different close old attribute (valid_to_date yesterday)
            # and make new attribute
            # Todo: combine the 2 command below into one transaction
            _close_attribute(existing_attribute)
        _add_new_attribute(attribute, debug=debug)

    else:
        raise ValueError(
            f"Attrubute type '{attribute.attribute_type}' does not exist.",
            "No records added to database.",
        )


def _get_attribute(attribute: Attribute) -> Optional[Attribute]:
    result = sql_query(
        f"""
        SELECT
            platform_property_id
          , attribute_type
          , bool_value
          , text_value
          , numeric_value
          , valid_from
          , valid_to
        FROM register.attributes
        WHERE platform_property_id = '{attribute.platform_property_id}'
        AND attribute_type = '{attribute.attribute_type}'
        AND CURRENT_DATE BETWEEN valid_from AND valid_to;
    """
    )
    # Deal with qery returing []
    if result:
        result = result[0]
    else:
        return

    return Attribute(
        platform_property_id=result[0],
        attribute_type=result[1],
        bool_value=result[2],
        text_value=result[3],
        numeric_value=result[4],
        valid_from=str(result[5]),
        valid_to=str(result[6]),
    )


def _close_attribute(
    attribute: Attribute, verbose: Optional[bool] = True
) -> None:
    sql_command(
        f"""
        UPDATE register.attributes 
        SET valid_to = CURRENT_DATE
        WHERE platform_property_id = {attribute.platform_property_id}
        AND attribute_type = '{attribute.attribute_type}';
    """
    )
    if verbose:
        print(
            f"{attribute.attribute_type} for property ",
            f"{attribute.platform_property_id} closed",
        )


def _add_new_attribute(
    attribute: Attribute,
    debug=False,
):
    fields = _fields_list(attribute)
    values = _collect_values(attribute)

    command = f"""
        INSERT INTO register.attributes({fields}) VALUES ({values});
    """
    if debug:
        print(command)
    else:
        sql_command(command)
        print("1 record writen to database")


def _attribute_type_exists(attribute_type: str) -> bool:
    """Checks if attribute exists in database"""
    results = sql_query("SELECT attribute_type FROM register.attribute_types;")
    attribute_types = [row[0] for row in results]

    return attribute_type in attribute_types


def _fields_list(attribute: Attribute) -> str:
    field_list = []
    for field_name, field_value in {
        "platform_property_id": attribute.platform_property_id,
        "attribute_type": attribute.attribute_type,
        "bool_value": attribute.bool_value,
        "text_value": attribute.text_value,
        "numeric_value": attribute.numeric_value,
        "valid_from": attribute.valid_from,
        "valid_to": attribute.valid_to,
    }.items():
        if field_value:
            # Get variable name (which is the actual name of the field)
            # KNOW BUG IN LINES BELOW: doesn't work!
            field_list.append(field_name)

    fields_string = ", ".join(field_list)
    return fields_string


def _collect_values(attribute: Attribute) -> str:
    all_fields = [
        attribute.platform_property_id,
        attribute.attribute_type,
        attribute.bool_value,
        attribute.text_value,
        attribute.numeric_value,
        attribute.valid_from,
        attribute.valid_to,
    ]
    not_null_fields = [field for field in all_fields if field]

    # Convert values to SQL format
    fields = [
        f"'{field}'" if isinstance(field, str) else field
        for field in not_null_fields
    ]
    # changing to string.lower() will catch bools and numeric
    fields = [str(field).lower() for field in fields]
    single_string = ", ".join(fields)

    return single_string


if __name__ == "__main__":
    add_attribute(
        platform_property_id=3, attribute_type="attribute_a", numeric_value=2
    )
