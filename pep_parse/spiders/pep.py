import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.xpath(
            '//section[@id="numerical-index"]'
        ).css('a::attr(href)').getall()
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get().split(' – ')
        if len(title) > 1:
            pep_number = int(title[0].replace('PEP', '').strip())
            pep_name = title[1].strip()

        data = {
            'number': pep_number,
            'name': pep_name,
            'status': response.css('dt:contains("Status") + dd::text').get(),
        }

        yield PepParseItem(data)
