# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class SaltosSpiderSelenium(scrapy.Spider):
    name = 'saltos_selenium'
    allowed_domains = ['ambito.com/contenidos/dolar.html']
    start_urls = ['https://www.ambito.com/contenidos/dolar.html']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        chrome_path = which("chromedriver")

        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.get("https://www.ambito.com/contenidos/dolar.html")

        self.html = driver.page_source
        driver.close()


    def parse(self, response):
        resp = Selector(text=self.html)
        for quedolar in resp.xpath(".//div[contains(@class, 'variacion-max-min-chico indicador')]"):
            yield {
                'fecha' : quedolar.xpath(".//span[@class='date-time data-fecha']/text()").get(),
                'titulo' : quedolar.xpath(".//div[@class='title-wrapper mr-2']/h2/a/text()").get(),
                'precioa_compra' : quedolar.xpath(".//span[contains(@class, 'value data-compra')]/text()").get(),
                'precioa_venta' : quedolar.xpath(".//span[contains(@class, 'value data-venta')]/text()").get(),
                'precio_solo' : quedolar.xpath(".//span[contains(@class, 'value data-valor')]/text()").get(),
                'variacion' : quedolar.xpath(".//span[contains(@class, 'percent data-class-variacion data-variacion text-nowrap text-right ')]/text()").get()
            }

