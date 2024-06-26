import scrapy
import psycopg2
from datetime import datetime as dt
from weather.functions import bofortToKm, convertDay, convertWindDir, CONNECTION


class OkairosHourlySpider(scrapy.Spider):
    name = 'okairos'

    with psycopg2.connect(CONNECTION) as conn:
        cursor = conn.cursor()

    def parse(self, response):
        # days = response.xpath('//div[@class="wnfp"]').getall()
        source = 'okairos.gr'
        city = response.xpath('//div[@id="intro-text"]/h2/text()').get().split()[3]
        data_columns = "(src, city, timecrawl, day, hour,  weather_cond, temperature, wind_km, wind_dir, yetos, cloudiness, humidity, air_pressure)"

        # tr are for different hours
        counter = 1
        for d in response.xpath('//div[@class="wnfp"]/h3/text()').getall():
            for i in range(2,
                           int(response.xpath('count(//*[@class="wnfp"]/table[' + str(counter) + ']//tr)').get()[:-2])):
                hour = response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[@class="hour"]/text()').get()
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
                yetos = ''
                try:
                    yetos = float(response.xpath('//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(
                        i) + ']/td[7]/text()').get().replace("\t", "").replace(",", ".")[:-2])
                except ValueError:
                    pass
                b = int(response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[5]/text()').get().strip())
                wind = float(bofortToKm(b))
                cloudiness = response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[8]/text()').get().strip()
                humidity = response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[9]/text()').get()
                air_pressure = response.xpath(
                    '//*[@class="wnfp"]/table[' + str(counter) + ']//tr[' + str(i) + ']/td[10]/text()').get().strip()
                timecrawl = dt.now()
                wind_dir = convertWindDir(wind_dir)
                day = convertDay(d)
                yield {
                    'src': source,
                    'city': city,
                    'timecrawl': timecrawl,
                    'day': day,
                    'hour': hour,
                    'weather_cond': weather_cond,
                    'temperature': temperature,
                    'wind_km': wind,
                    'wind_dir': wind_dir,
                    'yetos': yetos,
                    'cloudiness': cloudiness,
                    'humidity': humidity,
                    'air_pressure': air_pressure
                }
            counter = counter + 1
            query = "INSERT INTO okairosdata {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(data_columns)
            values = (source, city, timecrawl, day, hour, weather_cond, temperature, wind, wind_dir, yetos, cloudiness, humidity, air_pressure)
            self.cursor.execute(query, values)
        self.conn.commit()
        # response.xpath('count(//div[@class="wnfp"]/table)').get()

    def start_requests(self):
        yield scrapy.Request('https://www.okairos.gr/τρίπολη.html?v=ωριαία', self.parse)
        yield scrapy.Request('https://www.okairos.gr/γύθειο.html?v=ωριαία', self.parse)
        yield scrapy.Request('https://www.okairos.gr/καλαμάτα.html?v=ωριαία', self.parse)
        yield scrapy.Request('https://www.okairos.gr/κόρινθος.html?v=ωριαία', self.parse)
        yield scrapy.Request('https://www.okairos.gr/μεγαλόπολη.html?v=ωριαία', self.parse)

        # yield scrapy.Request('https://www.okairos.gr/ναύπλιο.html?v=ωριαία', self.parse)
        # yield scrapy.Request('https://www.okairos.gr/πάτρα.html?v=ωριαία', self.parse)
