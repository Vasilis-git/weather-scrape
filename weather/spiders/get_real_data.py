import scrapy
from datetime import datetime as dt
from ..functions import bofortToKm, convertDay


# Must run after 21:00, when site is updated
class okairosRealData(scrapy.Spider):
    name = 'get_real_data'

    def parse(self, response):
        source = 'okairos.gr'
        city = response.xpath('//div[@id="intro-text"]/h2/text()').get().split()[3]
        day = response.xpath('//div[@id="city-weather"]//thead//small/text()').get()
        b = int(response.xpath('//div[@id="city-weather"]//tbody/tr[5]/td[1]/text()').get().strip()[:-3])
        wind_km = bofortToKm(b)
        wind_dir = response.xpath('//div[@id="city-weather"]//tbody/tr[4]/td[1]/img/@src').get()[len('/img/icons/2_'):].split('.')[0]
        yetos = response.xpath('//div[@id="city-weather"]//tbody/tr[7]/td[1]/text()').get().strip()
        # every tr
        temp_counter = 1
        weather_cond_counter = 1
        for hour in response.xpath('//div[@id="city-weather"]//tbody/tr/th[@class="weather"][1]/text()').getall():
            hour = hour.strip()
            # response.xpath('//div[@id="city-weather"]//tbody/tr/th[@class="weather"][1]/../following-sibling::tr[1]/td[1]').get()
            temperature = float(response.xpath('//div[@id="city-weather"]//tbody/tr/th[@class="weather"][1]/../following-sibling::tr[1]/td[1]/div/text()')[temp_counter].get().strip()[:-1])
            weather_cond = response.xpath('//div[@id="city-weather"]//tbody/tr/th[@class="weather"][1]/../following-sibling::tr[1]/td[1]/p/text()')[weather_cond_counter].get().strip()
            temp_counter += 2
            weather_cond_counter += 3
            yield {
                'src': source,
                'city': city,
                'timecrawl': dt.now(),
                'day': convertDay(day),
                'hour': hour,
                'weather_cond': weather_cond,
                'temperature': temperature,
                'wind_km': wind_km,
                'wind_dir': wind_dir,
                'yetos': yetos
            }

    def start_requests(self):
        yield scrapy.Request('https://www.okairos.gr/τρίπολη.html', self.parse)
