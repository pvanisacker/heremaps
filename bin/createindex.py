__author__ = 'pieter'

import datetime
import os
import sys
import multiprocessing
from multiprocessing import Pool

from tools.reversegeocodershape import ReverseGeocoderShape


"""
    This file can be used for creating index files that speed up the reverse geocoding process.
    The index is actually on overlay of squares on top of the map.
    For each square we calculate which shapes/countries are part of that square.
    The bigger the squares the more shapes it will contain. That will make the index a bit less efficient.
    The smaller the squares the less shapes it will contain. This helps finding the shapes quicker.
    But making the squares too small will probably also have an adverse effect on performance.
    Because there will be too many squares to iterate through.

    The index step defines the size of the square in floating point degrees.
    An index step of 4 means the size of square will be 4 degrees.
    This is fine for a world country map.

    But if you have a map with shapes for a specific country you will not to reduce the index step.
    For example for the map of the French departements an index step of 2 is much better.
"""


def create_index(data):
    map_file = os.path.join("..", "appserver", "static", "data", data["file"])

    print("Change the line ending of %s" % data["file"])
    with open(map_file) as inp, open(map_file+"-tmp", 'w') as out:
        txt = inp.read()
        txt = txt.replace('\r\n', '\n')
        out.write(txt)
    os.remove(map_file)
    os.rename(map_file+"-tmp", map_file)

    rev = ReverseGeocoderShape()
    rev.load_map_file("geojson", map_file)
    rev.indexstep = data["step"]
    indexfile = os.path.join("lib", "reversegeocodeshape-" + rev.map_md5 + ".index")
    print("Creating index for file: %s md5sum: %s" % (data["file"], rev.map_md5))
    sys.stdout.flush()

    # try:
    #    os.remove(indexfile)
    # except OSError:
    #    pass

    start = datetime.datetime.now()
    rev.load_index_file(indexfile)
    end = datetime.datetime.now()
    delta = end - start
    print("Index creation for %s took %s seconds for %s" % (data["file"], delta.seconds, indexfile))
    sys.stdout.flush()

if __name__ == "__main__":
    shapes = []
    shapes.append({"file": "countries/be.geojson", "step": 2})
    shapes.append({"file": "countries/br.geojson", "step": 2})
    shapes.append({"file": "countries/ca.geojson", "step": 3})
    shapes.append({"file": "countries/cn.geojson", "step": 4})

    shapes.append({"file": "countries/de.geojson", "step": 2})
    shapes.append({"file": "countries/es.geojson", "step": 2})
    shapes.append({"file": "countries/fr.geojson", "step": 2})
    shapes.append({"file": "countries/in.geojson", "step": 4})
    shapes.append({"file": "countries/it.geojson", "step": 2})
    shapes.append({"file": "countries/ru.geojson", "step": 4})
    shapes.append({"file": "countries/uk.geojson", "step": 2})
    shapes.append({"file": "countries/us.geojson", "step": 3})
    shapes.append({"file": "countries/us_simplified.geojson", "step": 3})
    shapes.append({"file": "continents/africa.geojson", "step": 3})
    shapes.append({"file": "continents/asia.geojson", "step": 3})
    shapes.append({"file": "continents/europe.geojson", "step": 3})
    shapes.append({"file": "continents/north-america.geojson", "step": 3})
    shapes.append({"file": "continents/oceania.geojson", "step": 3})
    shapes.append({"file": "continents/south-america.geojson", "step": 3})

    shapes.append({"file": "world2.geojson", "step": 4})
    shapes.append({"file": "world3.geojson", "step": 4})
    shapes.append({"file": "squaremap_2.geojson", "step": 4})
    shapes.append({"file": "squaremap_4.geojson", "step": 8})
    shapes.append({"file": "hexagonmap_regeo_3.geojson", "step": 8})
    shapes.append({"file": "hexagonmap_regeo_2.geojson", "step": 4})
    shapes.append({"file": "hexagonmap_display_3.geojson", "step": 8})
    shapes.append({"file": "hexagonmap_display_2.geojson", "step": 4})

    # shapes.append({"file": "countries/us_counties.geojson", "step": 1})
    processing_count = multiprocessing.cpu_count()
    # processing_count=3
    print("Start creating indexes using %s workers" % processing_count)
    pool = Pool(processing_count)
    results = pool.map(create_index, shapes)
    pool.close()
    pool.join()
