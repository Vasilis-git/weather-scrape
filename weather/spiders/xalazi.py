import scrapy
from datetime import datetime as dt
# from lxml import html
# import requests
from ..functions import bofortToKm


def timeStrToInt(b):
    switcher = {
        "00": 0,
        "01": 1,
        "02": 2,
        "03": 3,
        "04": 4,
        "05": 5,
        "06": 6,
        "07": 7,
        "08": 8,
        "09": 9,

    }
    return switcher.get(b)


def parse_fog(response):
    fog = 'omixli'
    return fog


class XalaziSpider(scrapy.Spider):
    name = 'xalazi'
    # below link is for Tripoli
    # start_urls = ['http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1178']

    def parse(self, response):
        source = 'xalazi.gr'
        city = response.xpath('//div[@class="top"]/div[@class="name"]/text()').get()[len('Πρόγνωση 5 ημερών για '):]

        counter = 1
        day = ""
        for table_row in response.xpath('//table[@class="t orangered"]//tr').getall():
            try:
                day = response.xpath('//table[@class="t orangered"]/tr[' + str(counter) + ']/td[1]/text()')[
                    1].get().strip()
            except IndexError:
                pass  # do nothing
            hour = response.xpath('//*[@class="t orangered"]/tr[' + str(counter) + ']/td[2]//text()').get().strip()
            temperature = float(
                response.xpath('//*[@class="t orangered"]/tr[' + str(counter) + ']/td[3]//text()').get().strip()[:-2])
            humidity = float(
                response.xpath(
                    '//*[@class="t orangered"]/tr[' + str(counter) + ']/td[4]//text()').get().strip()[:-1])
            b = int(response.xpath('//*[@class="t orangered"]/tr[' + str(counter) + ']/td[5]//text()').get().split()[0])
            wind = float(bofortToKm(b))
            wind_dir = response.xpath('//*[@class="t orangered"]/tr[' + str(counter) + ']/td[5]//text()').get().split()[1][-2:]
            weather_cond = response.xpath('//*[@class="t orangered"]/tr[' + str(counter) + ']/td[6]/@title').get()
            yield {
                'src': source,
                'city': city,
                'timecrawl': dt.now(),
                'day': day,
                'hour': hour,
                'temperature': temperature,
                'wind_km': wind,
                'humidity': humidity,
                'wind_dir': wind_dir,
                'weather_cond': weather_cond
            }
            counter += 1

        # windends    = (rows[6].xpath('td//text()')[4].extract()).find(" ")
        # winddire    = (rows[6].xpath('td//text()')[4].extract()).find("at")
        # barometer = float()
        # yetos_index = int()
        # yetos = float()

        # direction = response.xpath('//*[@class="t orangered"]/tr[1]/td[5]//text()').get().replace("\r", "").replace(
        #   "\n", "")[windindex:].strip()

    def start_requests(self):

        # Τρίπολη
        yield scrapy.Request("http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1178", self.parse)
        # Μεγαλόπολη
        yield scrapy.Request("http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1067", self.parse)
        # Αίγιο
        yield scrapy.Request("http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=897", self.parse)
        # Γύθειο
        yield scrapy.Request('http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=914', self.parse)
        # Αμαλιάδα
        yield scrapy.Request('http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=987', self.parse)
        # Άστρος
        # yield scrapy.Request("http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=940", self.parse)
        # Ναύπλιο
        # yield scrapy.Request("http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1086", self.parse)
        # Δημητσάνα
        # yield scrapy.Request("http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=949", self.parse)
        # response = requests.get(self.start_urls[0])
        # tree = html.fromstring(response.content)
        # for link in tree.xpath('//div[@class="region-tree clearfix"]//li/a/@href'):
        #     yield scrapy.Request(link, self.parse)
