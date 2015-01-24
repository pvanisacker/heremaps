__author__ = 'pieter'

from shapely.geometry import Polygon

square_size = 2


def generatesquares():
    output = ""
    count = 0
    for lat in range(-90, 90, square_size):
        for lng in range(-180, 180, square_size):
            output += '{"type":"Feature","properties":{"id":"' + \
                str(count) + '"},"geometry":{"type":"MultiPolygon","coordinates":[[[[' + str(lng) + ',' + \
                str(lat) + '],[' + str(lng) + ',' + str(lat + square_size) + '],[' + str(lng + square_size) + ',' + \
                str(lat + square_size) + '],[' + str(lng + square_size) + ',' + str(lat) + '],[' + str(lng) + ',' + \
                str(lat) + ']]]]}},\n'
            count += 1
    return output[:-3] + '\n'


output = open("../appserver/static/data/squaremap_" + str(square_size) + ".geojson", "w")
output.write(
    '{"type":"FeatureCollection","crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84","needsindex":false}},"features":[\n')
output.write(generatesquares())
output.write("]}\n")
