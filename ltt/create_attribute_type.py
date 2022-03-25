from ltt.db_connections import sql_command


def create_attribute(attribute_type: str, description: str, data_type: str):
    """Adds a new attribute type to data base"""
    query = f"""
        INSERT INTO register.attribute_types VALUES 
            ('{attribute_type}', '{description}', '{data_type}');
    """
    print(query)
    sql_command(query)

    print(f"new attribute '{attribute_type}' added to database")


if __name__ == "__main__":
    attribute_type = input("attribute_type: ")
    description = input("description: ")
    data_type = input("data_type: ")

    create_attribute(attribute_type, description, data_type)
