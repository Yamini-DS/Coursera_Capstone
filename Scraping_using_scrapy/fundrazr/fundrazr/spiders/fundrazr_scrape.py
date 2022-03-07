import scrapy
from scrapy import signals
from scrapy.http import TextResponse
import urllib.parse as urllib
from fundrazr.items import FundrazrItem
from datetime import datetime
import re

import requests
import lxml.html

response=requests.get("https://in.seamsfriendly.com/collections/shorts")
print(response.text)

class Fundrazr(scrapy.Spider):
    name = "fundrazr"
    allowed_domains = ["in.seamsfriendly.com/"]

    # First Start Url
    start_urls = ["https://in.seamsfriendly.com/collections/shorts"]

    npages = 2

    # This mimics getting the pages using the next button.
    #for i in range(2, npages + 2):
     #   start_urls.append("https://in.seamsfriendly.com/collections/shorts=" + str(i) + "")

    def parse_dir_contents(self, response):
        item = FundrazrItem()

        # Getting Dress Title
        item['dressTitle'] = response.xpath(
            "//h2[contains(@class,'ProductItem__Title Heading')]/descendant::text()").extract()

        # Getting description
        item['description'] = response.xpath(
            "//div[contains(@class,'label_icon label_icon-mob orgc')]/descendant::text()").extract()

        # getting price
        item['price'] = response.xpath(
            "//div[contains(@class,'ProductItem__PriceList  Heading')]//span[contains(@class,'ProductItem__Price Price Text--subdued')]/descendant::text()").extract()

        # getting urls
        item['url'] = [urllib.urljoin(response.url, src) for src in response.xpath('//img/@src').extract()]

        # Getting dress title after removing the extra text
        title_only = response.xpath("//h2[contains(@class,'ProductItem__Title Heading')]/descendant::text()").extract()
        title_only = [x.strip() for x in title_only if len(x.strip()) > 0]
        # item['title_only']  = " ".join(title_only)
        item['dressTitle'] = title_only

        yield item
