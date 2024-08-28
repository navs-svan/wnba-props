# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WnbaScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PlayerProps(scrapy.Item):
    name = scrapy.Field()
    minutes = scrapy.Field()
    field_goals = scrapy.Field()
    fg_attemps = scrapy.Field()
    fg_percent = scrapy.Field()
    fg_three = scrapy.Field()
    fg_three_attempts = scrapy.Field()
    fg_three_percent = scrapy.Field()
    rb_offensive = scrapy.Field()
    rb_total = scrapy.Field()
    assists = scrapy.Field()
    steals = scrapy.Field()
    blocks = scrapy.Field()
    turnovers = scrapy.Field()
    personal_fouls = scrapy.Field()
    points = scrapy.Field()
    plus_minus = scrapy.Field()

    true_shoot_percent = scrapy.Field()
    efg_percent = scrapy.Field()
    three_pt_attempt = scrapy.Field()
    ft_attempt = scrapy.Field()
    rb_off_percent = scrapy.Field()
    rb_def_percent = scrapy.Field()
    rb_tot_percent = scrapy.Field()
    assist_percent = scrapy.Field()
    steal_percent = scrapy.Field()
    block_percent = scrapy.Field()
    turnover_percent = scrapy.Field()
    usage_percent = scrapy.Field()
    off_rating = scrapy.Field()
    def_rating = scrapy.Field()

    home_court = scrapy.Field()
    date = scrapy.Field()
    team = scrapy.Field()
