import scrapy
from datetime import datetime as dt
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
    return switcher.get(b, b)


def parse_fog(response):
    fog = 'omixli'
    return fog


class XalaziSpider(scrapy.Spider):
    name = 'xalazi_spider'
    allowed_domains = ['xalazi.gr']
    # below link is for Tripoli
    start_urls = ['http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1178']

    def parse(self, response):
        source = 'xalazi.gr'
        city = response.xpath('//div[@class="top"]/div[@class="name"]/text()').get().split()[4]

        counter = 1
        date = ""
        for table_row in response.xpath('//table[@class="t orangered"]//tr').getall():
            try:
                date = response.xpath('//table[@class="t orangered"]/tr[' + str(counter) + ']/td[1]/text()')[
                    1].get().replace(
                    "\r\n", "")
            except IndexError:
                pass  # do nothing

            print(date)
            counter += 1

        hour = response.xpath('//*[@class="t orangered"]/tr[1]/td[2]//text()').get().replace("\r", "").replace("\n",
                                                                                                               "").strip()[
               :2]

        day = response.xpath('//table[@class="t orangered"]/tr[1]/td[1]/text()')[1].get().replace("\r", "").replace(
            "\n", "").replace(" ", "")

        temperature = float(
            response.xpath('//*[@class="t orangered"]/tr[1]/td[3]//text()').get().replace("\r", "").replace("\n",
                                                                                                            "").strip()[
            :-2])
        humidity = float(
            response.xpath('//*[@class="t orangered"]/tr[1]/td[4]//text()').get().replace("\r", "").replace("\n",
                                                                                                            "").strip()[
            :-1])
        # windends    = (rows[6].xpath('td//text()')[4].extract()).find(" ")
        # winddire    = (rows[6].xpath('td//text()')[4].extract()).find("at")
        barometer = float()
        yetos_index = int()
        yetos = float()
        windindex = int(response.xpath('//*[@class="t orangered"]/tr[1]/td[5]//text()').get().find(" "))
        direction = response.xpath('//*[@class="t orangered"]/tr[1]/td[5]//text()').get().replace("\r", "").replace(
            "\n", "")[windindex:].strip()
        b = int(
            response.xpath('//*[@class="t orangered"]/tr[1]/td[5]//text()').get().replace("\r", "").replace("\n", "")[
            :windindex].strip())
        wind = float(bofortToKm(b))
        """
        yield {
            'src': source,
            'city': city,
            'timecrawl': dt.now(),
            'day': day,
            'hour': hour,
            'temperature': temperature,
            'wind_km': wind,
            'humidity': humidity,
            'barometer': barometer,
            'yetos': yetos
        }
        """

    def start_requests(self):
        # Τρίπολη
        yield scrapy.Request('http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1178',
                             self.parse)
