import psycopg2

CONNECTION = "postgres://sensors:DKM-sensors37@localhost:5432/sensors"

with psycopg2.connect(CONNECTION) as conn:
    cursor = conn.cursor()

data_columns = "(src, city, timecrawl, day, hour, temperature, wind_km, humidity, wind_dir, weather_cond)"
query = "INSERT INTO xalazidata {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(data_columns)
values = ('source', 'city', '2024-05-24 00:00:02.741949', 'day', 'hour', '21.0', '16.0', '38.0', 'wind_dir', 'weather_cond')
cursor.execute(query, values)
conn.commit()
