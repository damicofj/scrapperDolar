# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class SaltosSpider(scrapy.Spider):
    name = 'saltos'
    allowed_domains = ['ambito.com/contenidos/dolar.html']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(5))
  
            -- splash:set_viewport_full()
            return {
            -- image = splash:png(),
            html = splash:html()
            }
        end

    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.ambito.com/contenidos/dolar.html", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        for quedolar in response.xpath(".//div[contains(@class, 'variacion-max-min-chico indicador')]"):
            yield {
                'fecha' : quedolar.xpath(".//span[@class='date-time data-fecha']/text()").get(),
                'titulo' : quedolar.xpath(".//div[@class='title-wrapper mr-2']/h2/a/text()").get(),
                'precioa_compra' : quedolar.xpath(".//span[contains(@class, 'value data-compra')]/text()").get(),
                'precioa_venta' : quedolar.xpath(".//span[contains(@class, 'value data-venta')]/text()").get(),
                'precio_solo' : quedolar.xpath(".//span[contains(@class, 'value data-valor')]/text()").get(),
                'variacion' : quedolar.xpath(".//span[contains(@class, 'percent data-class-variacion data-variacion text-nowrap text-right ')]/text()").get()
            }

