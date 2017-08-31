# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChamberOfDeputiesAmendment(scrapy.Item):
    _id = scrapy.Field()
    application_method_id = scrapy.Field()
    author = scrapy.Field()
    code = scrapy.Field()
    description = scrapy.Field()
    expenditure_group_id = scrapy.Field()
    page_number = scrapy.Field()
    party = scrapy.Field()
    pdfs = scrapy.Field()
    commitment_info_url = scrapy.Field()
    state = scrapy.Field()
    target_location = scrapy.Field()
    urls = scrapy.Field()
    value = scrapy.Field()
    year = scrapy.Field()
