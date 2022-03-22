import datetime
from typing import Optional, Union
from ltt.db_connections import sql_query, sql_command


def add_addtribute(
    wra_property_id: int,
    attribute_type: str,
    bool_value: Optional[bool] = None,
    text_value: Optional[str] = None,
    numeric_value: Optional[Union[int, float]] = None,
    valid_from: Optional[str] = str(datetime.date.today()),
    valid_to: Optional[str] = None,
    debug=False,
):
    if _attribute_exists(attribute_type):
        fields = _fields_list(
            wra_property_id,
            attribute_type,
            bool_value,
            text_value,
            numeric_value,
            valid_from,
            valid_to,
        )
        values = _collect_values(
            wra_property_id,
            attribute_type,
            bool_value,
            text_value,
            numeric_value,
            valid_from,
            valid_to,
        )

        command = f"""
            INSERT INTO register.attributes({fields}) VALUES ({values});
        """
        if debug:
            print(command)
        else:
            sql_command(command)
            print("1 record writen to database")

    else:
        raise ValueError(
            f"Attrubute type '{attribute_type}' does not exist.",
            "No records added to database.",
        )


def _attribute_exists(attribute_type: str) -> bool:
    """Checks if attribute exists in database"""
    results = sql_query("SELECT attribute_type FROM register.attribute_types;")
    attribute_types = [row[0] for row in results]

    return attribute_type in attribute_types


def _fields_list(
    wra_property_id: int,
    attribute_type: str,
    bool_value: Optional[bool] = None,
    text_value: Optional[str] = None,
    numeric_value: Optional[Union[int, float]] = None,
    valid_from: Optional[str] = str(datetime.date.today()),
    valid_to: Optional[str] = None,
) -> str:
    field_list = []
    for field in [
        wra_property_id,
        attribute_type,
        bool_value,
        text_value,
        numeric_value,
        valid_from,
        valid_to,
    ]:
        if field:
            # Get variable name (which is the actual name of the field)
            field_name = [
                name for name, value in locals().items() if value == field
            ][0]
            field_list.append(field_name)

    fields_string = ", ".join(field_list)
    return fields_string


def _collect_values(
    wra_property_id: int,
    attribute_type: str,
    bool_value: Optional[bool] = None,
    text_value: Optional[str] = None,
    numeric_value: Optional[Union[int, float]] = None,
    valid_from: Optional[str] = str(datetime.date.today()),
    valid_to: Optional[str] = None,
) -> str:
    all_fields = [
        wra_property_id,
        attribute_type,
        bool_value,
        text_value,
        numeric_value,
        valid_from,
        valid_to,
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
    add_addtribute(
        wra_property_id=3, attribute_type="attribute_a", numeric_value=2
    )
