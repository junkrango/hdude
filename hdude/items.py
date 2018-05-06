# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Field, Item


class HdudeItem(Item):
    name = Field()
    url = Field()
    like_count = Field()
    view_count = Field()
    cover_image = Field()
    tags = Field()
    source = Field()
    sources = Field()
