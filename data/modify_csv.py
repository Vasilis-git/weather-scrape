import csv

# Read the existing CSV file and store its content
csv_file_path = 'xalazi.csv'
with open(csv_file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = list(reader)

default = ""

# Add the new columns headers to the first row of the data
data[0].append('wind_dir')
data[0].append('weather_cond')

# Add the new columns values to the remaining rows
for i in range(1, len(data)):
    data[i].append(default)
    data[i].append(default)

# Write the updated data back to the CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)
