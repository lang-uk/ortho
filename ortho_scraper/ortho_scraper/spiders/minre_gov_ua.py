import scrapy
from urllib.parse import urlparse
from scrapy.loader import ItemLoader
from ortho_scraper.items import OrthoScraperItem


class MinreGovUaSpider(scrapy.spiders.SitemapSpider):
    name = "minre_gov_ua"
    allowed_domains = ["minre.gov.ua"]
    start_urls = ["https://minre.gov.ua"]

    sitemap_urls = ["https://minre.gov.ua/wp-sitemap.xml"]
    sitemap_follow = [r"posts"]

    def parse(self, response):
        loader = ItemLoader(item=OrthoScraperItem(), response=response)

        # Get all alternate URLs
        loader.add_css("versions", "link[rel=alternate][hreflang]::attr(href)")

        # Get publish date
        loader.add_css("publish_date", ".published::text")

        # Get title
        loader.add_css("title", ".heading h1::text")

        # Get content
        loader.add_css("text", ".text-content > *")

        # Determine language
        url_path = urlparse(response.url).path
        lang = "uk"  # default
        if "/crh/" in url_path:
            lang = "crh"
        elif "/en/" in url_path:
            lang = "en"

        loader.add_value("lang", lang)
        loader.add_value("url", response.url)
        loader.add_value("path", url_path)

        yield loader.load_item()
