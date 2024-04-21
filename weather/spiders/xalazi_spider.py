import scrapy
from datetime import datetime as dt


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
        city = 'Tripoli'
        hour = response.xpath('//*[@class="t orangered"]/tr[1]/td[2]//text()').get().replace("\r", "").replace("\n",
                                                                                                               "").strip()[
               :2]
        hour = int(timeStrToInt(hour))
        crawldate = dt.now()
        if (hour == 0):
            cdate = dt.now()  # +  datetime.timedelta(days = 1)
        else:
            cdate = dt.now()
        year = int(cdate.year)
        month = int(timeStrToInt(
            response.xpath('//*[@class="t orangered"]/tr[1]/td[1]//text()')[1].get().replace("\r", "").replace("\n",
                                                                                                               "").strip()[
            3:]))
        day = int(timeStrToInt(
            response.xpath('//*[@class="t orangered"]/tr[1]/td[1]//text()')[1].get().replace("\r", "").replace("\n",
                                                                                                               "").strip()[
            :2]))

        time = dt(year, month, day, int(hour), 0) - datetime.timedelta(hours=3, minutes=0)
        timeutc = dt(year, month, day, int(hour), 0)
        timestr = timeutc.strftime("%d/%m/%Y, %H:%M")
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

        yield {
            'src': source,
            'city': city,
            'timecrawl': dt.now(),
            'day': convertDay(day),
            'hour': hour,
            'temperature': temperature,
            'wind_km': wind,
            'humidity': humidity,
            'barometer': barometer,
            'yetos': yetos
        }

    def start_requests(self):
        yield scrapy.Request('http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1178',
                             self.parse)
