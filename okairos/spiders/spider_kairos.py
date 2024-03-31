import scrapy
from scrapy.spiders import CrawlSpider


class CrawlingSpider(CrawlSpider):
    name = "mycrawler"

    # allowed_domains = ["okairos.gr"]
    # start_urls = ["https://okairos.gr/πελοπόννησος/"]

    # rules = (
    #    Rule(LxmlLinkExtractor(allow="τρίπολη.html"), callback="parse_item"),
    # )

    def start_requests(self):
        yield scrapy.Request(url='https://okairos.gr/τρίπολη.html', callback=self.parse_list)

    @staticmethod
    def parse_list(response):
        max_temp_list = response.css(".max-ln2::text").getall()
        min_temp_list = response.css(".min-ln1::text").getall()
        counter = 0
        for item_selector in response.css(".cw-14-days small::text").getall():
            item = {
                'date': item_selector,
                'max-temp': max_temp_list[counter].replace("\n", "").replace("\t", "").replace(" ", ""),
                'min-temp': min_temp_list[counter].replace("\n", "").replace("\t", "").replace(" ", "")
            }
            counter = counter + 1
            yield item

        # yield {
        #    "date": response.css(".cw-14-days small::text").get(),
        #    "max-temp": response.css(".max-ln2::text").get().replace("\n", "").replace("\t", "").replace(" ", "")
        #    "min-temp": response.css(".min-ln1::text").get().replace("\n", "").replace("\t", "").replace(" ", "")
        # }

# response.css("#province-navigation .province- a[href]::text").getall()
