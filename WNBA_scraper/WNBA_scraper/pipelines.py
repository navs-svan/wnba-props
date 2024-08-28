# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import psycopg2

class WnbaScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # convert date to proper format
        format = '%a, %B %d, %Y'
        value = adapter.get("date")
        date = datetime.datetime.strptime(value, format)
        adapter["date"] = date.date()

        return item

class PostgresPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        # Start Connection
        hostname = settings.get("DB_NAME")
        username = settings.get("DB_USER")
        password = settings.get("DB_PASS")
        database = settings.get("DB_DATA")
        
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, database=database)
        self.cur = self.connection.cursor()

        # Create Table
    #     self.cur.execute(""" 
    #             CREATE TABLE IF NOT EXISTS tracks(
    #             id serial PRIMARY KEY,
    #             chart_url TEXT,
    #             chart_name VARCHAR(128),
    #             chart_date TIMESTAMP,
    #             chart_author VARCHAR(128),
    #             track_title VARCHAR(128),
    #             track_artist VARCHAR(128),
    #             track_label VARCHAR(128),
    #             track_remixer VARCHAR(128) DEFAULT NULL,
    #             track_genre VARCHAR(128),
    #             track_bpm SMALLINT,
    #             track_key VARCHAR(128),
    #             track_date DATE,
    #             track_length_ms INTEGER
    #         )              
    #         """)

    # def process_item(self, item, spider):
    #     self.cur.execute("""INSERT INTO tracks (
    #                      chart_url,
    #                      chart_name,
    #                      chart_date,
    #                      chart_author,
    #                      track_title,
    #                      track_artist,
    #                      track_label,
    #                      track_remixer,
    #                      track_genre,
    #                      track_bpm,
    #                      track_key,
    #                      track_date,
    #                      track_length_ms 
    #                      ) VALUES (
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s,
    #                         %s 
    #                         )""", (
    #                      item["chart_url"],
    #                      item["chart_name"],
    #                      item["chart_date"],
    #                      item["chart_author"],
    #                      item["track_title"],
    #                      item["track_artist"],
    #                      item["track_label"],
    #                      item["track_remixer"],
    #                      item["track_genre"],
    #                      item["track_bpm"],
    #                      item["track_key"],
    #                      item["track_date"],
    #                      item["track_length_ms"]

    #                     ))

    #     self.connection.commit()
    #     return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()