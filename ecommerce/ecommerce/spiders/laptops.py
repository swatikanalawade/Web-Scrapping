#To create the project : scrapy startproject ecommerce
# To create spider: scrapy genspider https://www.johnlewis.com/browse/electricals/laptops-macbooks/view-all-laptops-macbooks/_/N-a8f
#To run Spider: scrapy crawl laptops


from typing import Iterable
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
import re
import math


class LaptopsSpider(scrapy.Spider):
    name = "laptops"
    allowed_domains = ["www.johnlewis.com"]
    start_urls = ["https://www.johnlewis.com/browse/electricals/laptops-macbooks/view-all-laptops-macbooks/_/N-a8f"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parsePage)

    def parsePage(self, response):
        per_page = 192
        per_chunck = 24
        hsx = Selector(text = response.text)
        product_count = int(re.findall(r'\d+', "".join(hsx.xpath('//*[@id = "screen-reader-updates"]//text()').extract()))[0])
        pages = math.ceil(product_count/per_page) #2
        # per_page_chuck = per_page/per_chunck #8
        remaining_prods = product_count
        for page_num in range(1, pages+1):
            if remaining_prods > per_page:
                this_page = per_page
                remaining_prods -= per_page
            else:
                this_page = remaining_prods
            total_chunks_per_page = math.ceil(this_page/per_chunck)
            yield scrapy.Request(url = f'{self.start_urls[0]}?page={page_num}&chunk={total_chunks_per_page}', callback=self.parse)

    def parse(self, response):
        hxs = Selector(text = response.text)
        links = hxs.xpath('//*[@class ="product-card_c-product-card__link__QeVVQ"]/@href').extract()
        for link in links:
            url_= 'https://'+ self.allowed_domains[0]+link
            yield scrapy.Request(url=url_,callback=self.parseProducts)

    def parseProducts(self, response):
        hxs = Selector(text = response.text)
        title = hxs.xpath('//*[@id="__next"]//h1//text()').extract()[0]
        price = hxs.xpath('//*[@class="ProductPrice_ProductPrice__Y8bXE"]//text()').extract()[0]
        specification = hxs.xpath('//*[@class = "ProductSpecificationAccordion_productSpecificationList__sf__7"]//div')
        import pdb;pdb.set_trace()
        yield {
            "title": title,
            "price": price
        }


# Command to output to json files ---> scrapy crawl laptops -o laptops.json
        
        
        
    