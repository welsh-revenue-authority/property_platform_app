import psycopg2
import os

from dotenv import load_dotenv

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


def sql_query(query: str):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    return result

def sql_query_json(query: str):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
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
