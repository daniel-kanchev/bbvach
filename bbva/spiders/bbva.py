import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bbva.items import Article


class BbvaSpider(scrapy.Spider):
    name = 'bbva'
    start_urls = ['https://www.bbva.ch/autor/communication-bbva-in-switzerland/']

    def parse(self, response):
        links = response.xpath('//div[@class="noticia"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('(//div[@class="noticia-tags"]//text())[last()]').get()
        if date:
            date = date.split('|')[-1].strip()

        content = response.xpath('//div[@class="noticia-contenido"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[1:]).strip()

        # author = response.xpath('').get()
        #
        # category = response.xpath('').get()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)
        # item.add_value('author', author)
        # item.add_value('category', category)

        return item.load_item()
