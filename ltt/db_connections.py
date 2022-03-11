import psycopg2
import os


def sql_query(query: str):
    connection = psycopg2.connect(
        user=os.environ.get("HEROKU_PGUSERNAME"),
        password=os.environ.get("HEROKU_PGPASSWORD"),
        host=os.environ.get("HEROKU_PGHOST"),
        port="5432",
        database=os.environ.get("HEROKU_PGDATABASE"),
    )
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    return result


if __name__ == "__main__":
    # Command line tool to query ltt_fiction database
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", type=str)

    query = parser.parse_args().query
    if query:
        result = sql_query(query)
        print(result)
