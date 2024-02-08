# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import psycopg2
import os


class RealestatePipeline:

    def __init__(self):
        load_dotenv()
        ## Connection Details
        hostname = os.environ["DB_HOST"]
        username = os.environ["DB_USER"]
        password = os.environ["DB_PASS"]
        database = os.environ["DB_NAME"]

        ## Create/Connect to database
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database
        )

        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        ## Create quotes table if none exists
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS apartments(
            id serial PRIMARY KEY, 
            img_url VARCHAR(255),
            name VARCHAR(255),
            location VARCHAR(255)
        )
        """
        )

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(
            """ insert into apartments (img_url, name, location) values (%s,%s,%s)""",
            (item["url"], str(item["name"]), item["location"]),
        )

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()
