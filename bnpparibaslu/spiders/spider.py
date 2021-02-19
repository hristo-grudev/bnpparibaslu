import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import BnpparibasluItem
from itemloaders.processors import TakeFirst


class BnpparibasluSpider(scrapy.Spider):
	name = 'bnpparibaslu'
	start_urls = ['https://wealthmanagement.bnpparibas/en/expert-voices.html']

	def parse(self, response):
		post_links = response.xpath('//div[@class="blocks"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@data-emptytext="Articlehead Component"]/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space() and not(ancestor::div[@class="pageseparator section"] | ancestor::div[@class="solutiondescription section"] | ancestor::div[@class="downloadLink section"] | ancestor::div[@class="solutions section"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="date"]/span/text()').getall()
		date = [p.strip() for p in date]
		date = ' '.join(date).strip()
		if date:
			date = re.findall(r'\d+.\d+.\d+', date)[0]

		item = ItemLoader(item=BnpparibasluItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
