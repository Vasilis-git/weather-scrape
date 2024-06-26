import scrapy
import psycopg2
from datetime import datetime as dt

from ..functions import convertDay, CONNECTION


class Meteo_Data(scrapy.Spider):
    name = "meteo"
    with psycopg2.connect(CONNECTION) as conn:
        cursor = conn.cursor()

    def parse(self, response):
        source = "meteo.gr"
        city = response.xpath('//*[@class="cityname flleft01"]/text()').get()

        all_hours = response.xpath('//tr[@class="perhour rowmargin"]/td[1]//tr/td[1]/text()').getall()
        all_temps = response.xpath('//tr[@class="perhour rowmargin"]/td[2]/div/text()[1]').getall()
        all_humid = response.xpath('//tr[@class="perhour rowmargin"]/td[2]/div/div/text()').getall()
        all_wind_km = response.xpath('//tr[@class="perhour rowmargin"]/td[4]//tr/td[1]/span/text()[1]').getall()
        all_wind_dirs = response.xpath('//tr[@class="perhour rowmargin"]/td[4]//tr/td[1]/text()[1]').getall()
        all_wthr_cond = response.xpath('//tr[@class="perhour rowmargin"]/td[5]//tr[3]/td/text()[1]').getall()
        month_days = response.xpath('//div[@class="content"]//span[@class="dayNumbercf"]/text()[1]').getall()
        month_names = response.xpath('//div[@class="content"]//span[@class="monthNumbercf"]/text()').getall()
        day_counter = 0
        total_rows = int(response.xpath('count(//tr[@class="perhour rowmargin"])').get().split('.')[0])
        data_columns = "(src, city, timecrawl, day, hour, temperature, humidity, wind_km, wind_dir, weather_cond)"
        for tr_counter in range(0, total_rows):
            hour = all_hours[tr_counter]
            month_name = month_names[day_counter].strip()
            month_day = month_days[day_counter]
            day = month_day + " " + month_name
            temperature = all_temps[tr_counter]
            humidity = all_humid[tr_counter]
            wind_km = all_wind_km[tr_counter].split()[0]
            if wind_km == 'km/h':
                wind_km = ''
            wind_dir = all_wind_dirs[tr_counter][-2:].replace(' ', '')
            weather_cond = all_wthr_cond[tr_counter][:-1]

            timecrawl = dt.now()
            day = convertDay(day)
            yield {
                'src': source,
                'city': city,
                'timecrawl': timecrawl,
                'day': day,
                'hour': hour,
                'temperature': temperature,
                'humidity': humidity,
                'wind_km': wind_km,
                'wind_dir': wind_dir,
                'weather_cond': weather_cond,
            }
            if hour == "21:00":
                day_counter += 1
            query = "INSERT INTO meteodata {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(data_columns)
            values = (source, city, timecrawl, day, hour, temperature, humidity, wind_km, wind_dir, weather_cond)
            self.cursor.execute(query, values)

        self.conn.commit()

    def start_requests(self):
        yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=37', self.parse)  # Άργος
        yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=36', self.parse)  # Τρίπολη
        yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=15', self.parse)  # Καλαμάτα
        yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=56', self.parse)  # Κόρινθος
        yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=58', self.parse)  # Σπάρτη
        yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=107', self.parse)  # Γύθειο
        yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=229', self.parse)  # Μεγαλόπολη
        yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=110', self.parse)  # Αίγιο
        yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=211', self.parse)  # Αμαλιάδα
        # yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=396', self.parse)  # Άστρος
        # yield scrapy.Request('https://meteo.gr/cf.cfm?city_id=10', self.parse)  # Πάτρα
