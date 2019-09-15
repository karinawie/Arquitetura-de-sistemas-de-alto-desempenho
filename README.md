Scrapy: baixando pdfs Enade

import scrapy
from scrapy.selector import Selector

class EnadeSpiderSpider(scrapy.Spider):
    name = 'enade_spider'
    start_urls = ['http://inep.gov.br/web/guest/educacao-superior/enade/provas-e-gabaritos']

    def parse(self,response):
        base_url = 'http://inep.gov.br/web/guest/educacao-superior/enade/provas-e-gabaritos'
        # as chaves incluem o xpath abaixo, ou seja os anos, na parte que for no link
        session_urls = response.xpath('//*[@class="filter__year"]/option/@value').extract()
        # lista todos os eventos de acordo com o label        
        #//*[@id="p_p_id_56_INSTANCE_8m7JOS27it8a_"]/div/div/div[1]/div[14]/div[1]/a[3]

        for url in session_urls:
            next_url = base_url.format(url)
            yield scrapy.Request(url=next_url, callback=self.get_pdf)

    def get_pdf(self, response):
        #base_url = 'http://inep.gov.br'
        pdfs = response.xpath('//div/a[@target="_blank"]/@href').extract() 
        #//div/a[@target="_blank"]/@href --> mostra todos os links de pdfs
        # response.xpath('//div/a[@target="_blank"]/@href').extract() --> no terminal 

        for pdf in pdfs:
            print(pdf)
            yield scrapy.Request(url=pdf, callback=self.save_pdf)

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        print(path)
        self.logger.info("Saving PDF %s", path)
        with open(path, 'wb') as f:
            f.write(response.body)
