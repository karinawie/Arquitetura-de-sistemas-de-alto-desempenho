#script com Scrapy para recolher PDFs. Fontes dos dados no INEP: Relatórios
#este script baixa todos os PDFs do ano de 2006

import scrapy
from scrapy.selector import Selector

class EnadeSpiderSpider(scrapy.Spider):
    name = 'enade_spider'
    start_urls = ['http://inep.gov.br/web/guest/relatorios']

    def parse(self,response):
        base_url = 'http://inep.gov.br/web/guest/relatorios'
        # as chaves incluem o xpath abaixo, ou seja os anos, na parte que for no link
        session_urls = response.xpath('//*[@class="filter__year"]/option/@value').extract()       

        for url in session_urls:
            next_url = base_url.format(url)
            yield scrapy.Request(url=next_url, callback=self.get_pdf)

    def get_pdf(self, response):
        #pdfs = response.xpath('//*[@data-nav="2010"]/div/a[@target="_blank"]/@href').extract()
        pdfs = response.xpath('//*[@data-nav="2006"]/div/ul/a[@target="_blank"]/@href').extract()

        for pdf in pdfs:
            print(pdf)
            yield scrapy.Request(url=pdf, callback=self.save_pdf)

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        print(path)
        self.logger.info("Saving PDF %s", path)
        with open(path, 'wb') as f:
            f.write(response.body)
           
# scrapy runspider relatorios.py
