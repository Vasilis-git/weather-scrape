import scrapy
from datetime import datetime as dt
from ..functions import bofortToKm, convertDay


class OkairosHourlySpider(scrapy.Spider):
    name = 'hourly_spider'
    allowed_domains = ['okairos.gr']
    start_urls = ['https://www.okairos.gr/τρίπολη.html?v=ωριαία']

    def parse(self, response):
        # days = response.xpath('//div[@class="wnfp"]').getall()
        source = 'okairos.gr'
        city = response.xpath('//div[@id="intro-text"]/h2/text()').get().split()[3]
        # time = dt(year, month, day, int(hour), 0) - datetime.timedelta(hours=3, minutes=0)
        # timeutc = dt(year, month, day, int(hour), 0)
        # timestr = timeutc.strftime("%d/%m/%Y, %H:%M")

        # tr are for different hours
        counter = 1
        for day in response.xpath('//div[@class="wnfp"]/h3/text()').getall():
            for i in range(2,
                           int(response.xpath('count(//*[@class="wnfp"]/table[' + str(counter) + ']//tr)').get()[:-2])):
                hour = response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[@class="hour"]/text()').get()
                if hour != "8:00" and hour != "14:00" and hour != "20:00":
                    continue
                wind_dir = ""
                try:
                    wind_dir = response.xpath(
                        '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[4]/div/@class').get()[
                            len('wind-1'):]
                except TypeError:
                    pass
                weather_cond = response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[2]/div/@title').get()

                temperature = float(response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[3]/div/text()').get()[:-1])
                # humidity = float(response.xpath(
                # '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[9]/text()').get()[:-1])
                # barometer = float(
                # response.xpath('//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(
                #     i) + ']/td[10]/text()').get().replace("\n", "").replace("\t", "")[:-4])
                yetos = float(response.xpath('//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(
                    i) + ']/td[7]/text()').get().replace("\t", "").replace(",", ".")[:-2])
                b = int(response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[5]/text()').get().strip())
                wind = float(bofortToKm(b))

                yield {
                    # 'id': source + ' ' + timestr,
                    'src': source,
                    'city': city,
                    # 'time': time,
                    'timecrawl': dt.now(),
                    'day': convertDay(day),
                    'hour': hour,
                    'weather_cond': weather_cond,
                    'temperature': temperature,
                    'wind_km': wind,
                    'wind_dir': wind_dir,
                    # 'humidity': humidity,
                    # 'barometer': barometer,
                    'yetos': yetos
                }
            counter = counter + 1

        # response.xpath('count(//div[@class="wnfp"]/table)').get()

    def start_requests(self):
        yield scrapy.Request('https://www.okairos.gr/τρίπολη.html?v=ωριαία', self.parse)
        # yield scrapy.Request('https://www.okairos.gr/μεγαλόπολη.html?v=ωριαία', self.parse)
        # yield scrapy.Request('https://www.okairos.gr/βυτίνα.html?v=ωριαία', self.parse)
        # yield scrapy.Request('https://www.okairos.gr/καλαμάτα.html?v=ωριαία', self.parse)
        # yield scrapy.Request('https://www.okairos.gr/κόρινθος.html?v=ωριαία', self.parse)
