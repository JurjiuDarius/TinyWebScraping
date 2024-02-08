import scrapy
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor


class ApartmentsSpider(scrapy.Spider):
    name = "apartments"
    allowed_domains = ["sreality.cz"]
    start_urls = ["https://sreality.cz/en/search/for-sale/apartments"]
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse,
                dont_filter=True,
            )

    # def parse(self, response):
    #     ok = ""
    #     self.log("The url is " + response.url)
    #     self.log(response.body)
    #     yield response.body

    def parse(self, response):
        if response.url[-2:].isdigit() and int(response.url[-2:]) > 26:
            return

        self.driver.get(response.url)

        ## Wait for elements to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.property-list"))
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="page-layout"]/div[2]/div[3]/div[3]/div/div/div/div/div[3]/div/div[22]/ul[1]/li[12]/a',
                )
            )
        )
        properties = self.driver.find_elements(By.CSS_SELECTOR, "div.property")
        filename = f"images-{response.url[-2:]}.txt"

        with open(filename, "a+", encoding="utf-8") as f:
            # Selector for all the names from the link with class 'ng-binding'
            for property in properties:
                img = property.find_element(By.XPATH, "./preact/div/div[1]/a[1]/img")
                img_source = img.get_attribute("src")
                property_name = property.find_element(
                    By.XPATH, "./div/div/span/h2/a"
                ).text
                property_location = property.find_element(
                    By.XPATH, "./div/div/span/span[1]"
                ).text

                yield {
                    "url": img_source,
                    "name": property_name,
                    "location": property_location,
                }

        ##Go to the next page
        next_button = self.driver.find_element(
            By.XPATH,
            '//*[@id="page-layout"]/div[2]/div[3]/div[3]/div/div/div/div/div[3]/div/div[22]/ul[1]/li[12]/a',
        )
        href = next_button.get_attribute("href")
        yield Request(href, self.parse)
