import psycopg2
from dotenv import load_dotenv
import os


def fetch_apartments():
    load_dotenv()
    hostname = os.environ["DB_HOST"]
    username = os.environ["DB_USER"]
    password = os.environ["DB_PASS"]
    database = os.environ["DB_NAME"]
    connection = psycopg2.connect(
        host=hostname, user=username, password=password, dbname=database
    )

    with connection.cursor() as curs:

        try:

            curs.execute("SELECT * from apartments")

            many_rows = curs.fetchmany(500)

            return many_rows

        except Exception as e:
            print(e)
