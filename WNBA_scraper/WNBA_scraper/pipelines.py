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
        format = '%a, %b %d, %Y'
        date_value = adapter.get("date")
        date = datetime.datetime.strptime(date_value, format)
        adapter["date"] = date.date()

        # add hours to gametime
        time_value = adapter.get("minutes")
        gametime = "00:" + time_value
        adapter["minutes"] = gametime

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
        self.cur.execute(""" 
                CREATE TABLE IF NOT EXISTS props(
                    id serial PRIMARY KEY,
                    date DATE,
                    home_court BOOLEAN,
                    team VARCHAR(64),
                    opponent VARCHAR(64),
                    name VARCHAR(64),
                    minutes TIME,
                    field_goals INTEGER DEFAULT 0,
                    fg_attempts INTEGER DEFAULT 0,
                    fg_percent NUMERIC DEFAULT 0.0,
                    fg_three INTEGER DEFAULT 0,
                    fg_three_attempts INTEGER DEFAULT 0,
                    fg_three_percent NUMERIC DEFAULT 0.0,
                    rb_offensive INTEGER DEFAULT 0,
                    rb_total INTEGER DEFAULT 0,
                    assists INTEGER DEFAULT 0,
                    steals INTEGER DEFAULT 0,
                    blocks INTEGER DEFAULT 0,
                    turnovers INTEGER DEFAULT 0,
                    personal_fouls INTEGER DEFAULT 0,
                    points INTEGER DEFAULT 0,
                    plus_minus INTEGER DEFAULT 0,
                    true_shoot_percent NUMERIC DEFAULT 0.0,
                    efg_percent NUMERIC DEFAULT 0.0,
                    three_pt_attempt NUMERIC DEFAULT 0.0,
                    ft_attempt NUMERIC DEFAULT 0.0,
                    rb_off_percent NUMERIC DEFAULT 0.0,
                    rb_def_percent NUMERIC DEFAULT 0.0,
                    rb_tot_percent NUMERIC DEFAULT 0.0,
                    assist_percent NUMERIC DEFAULT 0.0,
                    steal_percent NUMERIC DEFAULT 0.0,
                    block_percent NUMERIC DEFAULT 0.0,
                    turnover_percent NUMERIC DEFAULT 0.0,
                    usage_percent NUMERIC DEFAULT 0.0,
                    off_rating INTEGER DEFAULT 0,
                    def_rating INTEGER DEFAULT 0
            )              
            """)
        
        self.connection.commit()

    def process_item(self, item, spider):
        try:
            self.cur.execute("""INSERT INTO props(
                            date,
                            home_court,
                            team,
                            opponent,
                            name,
                            minutes,
                            field_goals,
                            fg_attempts,
                            fg_percent,
                            fg_three,
                            fg_three_attempts,
                            fg_three_percent,
                            rb_offensive,
                            rb_total,
                            assists,
                            steals,
                            blocks,
                            turnovers,
                            personal_fouls,
                            points,
                            plus_minus,
                            true_shoot_percent,
                            efg_percent,
                            three_pt_attempt,
                            ft_attempt,
                            rb_off_percent,
                            rb_def_percent,
                            rb_tot_percent,
                            assist_percent,
                            steal_percent,
                            block_percent,
                            turnover_percent,
                            usage_percent,
                            off_rating,
                            def_rating
                            ) VALUES (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                                )""", (
                            item["date"],
                            item["home_court"],
                            item["team"],
                            item["opponent"],
                            item["name"],
                            item["minutes"],
                            item["field_goals"],
                            item["fg_attempts"],
                            item["fg_percent"],
                            item["fg_three"],
                            item["fg_three_attempts"],
                            item["fg_three_percent"],
                            item["rb_offensive"],
                            item["rb_total"],
                            item["assists"],
                            item["steals"],
                            item["blocks"],
                            item["turnovers"],
                            item["personal_fouls"],
                            item["points"],
                            item["plus_minus"],
                            item["true_shoot_percent"],
                            item["efg_percent"],
                            item["three_pt_attempt"],
                            item["ft_attempt"],
                            item["rb_off_percent"],
                            item["rb_def_percent"],
                            item["rb_tot_percent"],
                            item["assist_percent"],
                            item["steal_percent"],
                            item["block_percent"],
                            item["turnover_percent"],
                            item["usage_percent"],
                            item["off_rating"],
                            item["def_rating"]
                            ))
        except psycopg2.errors.InFailedSqlTransaction:
           self.cur.execute("ROLLBACK")

        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()