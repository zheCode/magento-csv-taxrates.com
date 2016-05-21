import csv
import time

now = time.strftime('%Y-%m-%d %H:%M:%S')

# Original file located at: http://www.taxrates.com/state-rates/california/?referrer=https://www.google.com/&lastReferrer=www.taxrates.com
# Must be sorted in order of increasing zip code!
rawFileLocation = 'Raw-CSVs/CA-Raw-Taxrates-05-2016.csv'
parsedFileLocation = 'Parsed-CSVs/' + now + '.csv'

inputFile = open(rawFileLocation)
outputFile = open(parsedFileLocation, 'w')
reader = csv.reader(inputFile)
writer = csv.writer(outputFile)

country = "US"
readData = []
writeData = [["Code", "Country", "State", "Zip/Post Code", "Rate", "Zip/Post is Range", "Range From", "Range To", "default"]]

for row in reader:
    if reader.line_num > 1:
        readData.append({'state': row[0], 'zip': row[1], 'location': row[2], 'district': row[3], 'taxRate': str(float(row[4]) * 100)})

top = {}
recent = {}

# Parse line by line and merge as many lines as possible
for index, current in enumerate(readData):
    # Initialize top of stack if this is the first entry in the read data
    if index == 0:
        top = current
        recent = current
    else:
        # If it is the same locale, simply update the most recently viewed entry and continue parsing
        if recent['location'] == current['location'] and recent['district'] == current['district'] and recent['taxRate'] == current['taxRate']:
            recent = current
        # Else, if this is a distinct tax locale from the most recently viewed entry, add entry to write array
        else:
            # If there was only one distinct zip code in the current working group:
            if top['zip'] == recent['zip']:
                writeData.append({'code': recent['state'] + '-' + recent['zip'] + '-' + recent['location'].replace(' ', '-') + '-' + recent['district'], 'country': country, 'state': recent['state'], 'zip': recent['zip'], 'taxRate': recent['taxRate'], 'zipIsRange': '', 'zipFrom': '', 'zipTo': '', 'default': ''})
            # Else if this is a range of zip codes
            else:
                writeData.append({'code': current['state'] + '-' + top['zip'] + '-' + recent['zip'] + '-' + recent['location'].replace(' ', '-') + '-' + recent['district'], 'country': country, 'state': recent['state'], 'zip': top['zip'] + '-' + recent['zip'], 'taxRate': recent['taxRate'], 'zipIsRange': '1', 'zipFrom': top['zip'], 'zipTo': recent['zip'], 'default': ''})

            # And finish by resetting the stack
            top = current
            recent = current

for index, row in enumerate(writeData):
    # Just to see it ourselves in console
    print str(row)

    if index == 0:
        writer.writerow(row)
    else:
        writer.writerow([row['code'], row['country'], row['state'], row['zip'], row['taxRate'], row['zipIsRange'], row['zipFrom'], row['zipTo'], row['default']])