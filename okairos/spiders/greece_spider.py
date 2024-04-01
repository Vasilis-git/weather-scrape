from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime as dt


class CrawlingSpider(CrawlSpider):
    name = "crawl_greece"
    allowed_domains = ['okairos.gr']
    start_urls = ['https://www.okairos.gr/']

    rules = (
        Rule(LinkExtractor(allow="", deny="κόσμος|υετός|δορυφόρος|νέφωση|θερμοκρασία|άνεμοι|πίεση")),
        Rule(LinkExtractor(allow="v=ωριαία"), callback="parse"),
    )

    def parse(self, response):
        source = 'okairos.gr'
        city = response.xpath('//div[@id="intro-text"]/h2/text()').get().split()[3]

        # tr are for different hours
        counter = 1;
        for day in response.xpath('//div[@class="wnfp"]/h3/text()').getall():
            for i in range(2,
                           int(response.xpath('count(//*[@class="wnfp"]/table[' + str(counter) + ']/tr)').get()[:-2])):
                hour = response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']/tr[' + str(i) + ']/td[@class="hour"]/text()').get()
                temperature = float(response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']/tr[' + str(i) + ']/td[3]/div/text()').get()[:-1])
                humidity = float(response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']/tr[' + str(i) + ']/td[9]/text()').get()[:-1])
                barometer = float(
                    response.xpath('//*[@class="wnfp"]/table[' + str(counter) + ']/tr[' + str(
                        i) + ']/td[10]/text()').get().replace("\n", "").replace("\t", "")[:-4])
                yetos = float(
                    response.xpath(
                        '//*[@class="wnfp"]/table[' + str(counter) + ']/tr[' + str(i) + ']/td[7]/text()').get().replace(
                        "\t", "").replace(",", ".")[:-2])
                b = int(response.xpath('//*[@class="wnfp"]/table[' + str(counter) + ']/tr[' + str(i) + ']/td[5]/text()').get().strip())
                wind = float(self.bofortToKm(b))

                yield {
                    # 'id': source + ' ' + timestr,
                    'src': source,
                    'city': city,
                    # 'time': time,
                    'timecrawl': dt.now(),
                    'day': convertDay(day),
                    'hour': hour,
                    'temperature': temperature,
                    'wind_km': wind,
                    'humidity': humidity,
                    'barometer': barometer,
                    'yetos': yetos
                }
            counter = counter + 1;

    @staticmethod
    def bofortToKm(b):
        switcher = {
            0: 1,
            1: 3.5,
            2: 8,
            3: 16,
            4: 25,
            5: 33,
            6: 45,
            7: 56,
            8: 69,
            9: 80,
            10: 96,
            11: 110,
            12: 124
        }
        return switcher.get(b, 0)


def convertDay(day):
    details = day.split()
    switcher = {
        "Απρ:": '4'
    }
    return str(int(details[1])) + '/' + switcher.get(details[2], details[2])