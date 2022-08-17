import psycopg2
import os

from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv()


def connect():
    """Returns connection"""
    connection = psycopg2.connect(
        user=os.environ.get("HEROKU_PGUSERNAME"),
        password=os.environ.get("HEROKU_PGPASSWORD"),
        host=os.environ.get("HEROKU_PGHOST"),
        port="5432",
        database=os.environ.get("HEROKU_PGDATABASE"),
    )
    return connection

def sql_insert(table, columns, data_rows, values):
    """Insert into DB."""
    connection = connect()
    cursor = connection.cursor()

    insert_statement = "INSERT INTO {table} ({columns}) VALUES ({values})".format(table=table, columns=columns, values=values)
    cursor.execute(insert_statement, data_rows)

    connection.commit()
    connection.close()

def sql_insert_bulk(table, columns, data_rows):
    """Bulk insert into DB. Skips duplicated rows by default."""
    connection = connect()
    cursor = connection.cursor()

    insert_statement = "INSERT INTO {table} ({columns}) VALUES %s ON CONFLICT DO NOTHING".format(table=table, columns=columns)

    execute_values(cursor, insert_statement, data_rows)
    #for d in data_rows:
    #    cursor.execute(insert_statement, d)

    connection.commit()
    connection.close()

def sql_query(query: str):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    return result

def sql_query_json(query: str, query_parameters: dict = None ):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query, query_parameters)
    #result = cursor.fetchall()
    result = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    connection.close()

    return result

def sql_command(command: str) -> None:
    """Executes command e.g. insert data"""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(command)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    # Command line tool to query ltt_fiction database
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", type=str)

    query = parser.parse_args().query
    if query:
        result = sql_query(query)
        print(result)
