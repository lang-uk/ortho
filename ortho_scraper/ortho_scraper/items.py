# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Join
from itemloaders.processors import MapCompose
from urllib.parse import urlparse


def clean_text(text):
    return text.replace("\xa0", "")


class OrthoScraperItem(scrapy.Item):
    versions = scrapy.Field(input_processor=MapCompose(lambda url: urlparse(url).path))

    title = scrapy.Field(
        input_processor=MapCompose(clean_text), output_processor=TakeFirst()
    )
    text = scrapy.Field(
        input_processor=MapCompose(clean_text), output_processor=Join("\n")
    )

    publish_date = scrapy.Field(output_processor=TakeFirst())
    lang = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    path = scrapy.Field(output_processor=TakeFirst())
