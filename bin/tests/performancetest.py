__author__ = 'pieter'

import csv
import datetime
from shapely.geometry import Point
from tools.reversegeocodershape import ReverseGeocoderShape

rev = ReverseGeocoderShape()
rev.load_map_file("geojson", "appserver/static/data/world2.geojson")

csv_max_count=100
print("Without index")
with open("lookups/latlng-data.csv", 'rb') as csvfile:
    reader = csv.reader(csvfile)
    start = datetime.datetime.now()
    count = 0
    for row in reader:
        count += 1
        if count == 1:
            continue
        print(rev.reversegeocodeshape(Point((float(row[0]), float(row[1])))))
        if count > csv_max_count:
            break

    stop = datetime.datetime.now()
    delta = stop-start
    print("Seconds: %s" % delta.seconds)
