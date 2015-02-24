__author__ = 'pieter'

import sys
sys.path.insert(1, '/home/pieter/git/heremaps/bin/')

import datetime
from shapely.geometry import Point
import csv
from tools.reversegeocodershape import ReverseGeocoderShape

csv_max_count = 100


def performance_test(csvfile, rev):
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
    delta = stop - start
    print("Seconds: %s" % delta.seconds)

print("Without index")
with open("lookups/latlng-data.csv", 'rb') as csvfile:
    rev = ReverseGeocoderShape()
    rev.load_map_file("geojson", "appserver/static/data/world2.geojson")

    performance_test(csvfile, rev)

print("With index")
with open("lookups/latlng-data.csv", 'rb') as csvfile:
    rev = ReverseGeocoderShape()
    rev.load_map_file("geojson", "appserver/static/data/world2.geojson")
    rev.load_index("bin/lib")

    performance_test(csvfile, rev)
