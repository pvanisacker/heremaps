__author__ = 'pieter'
import os
import hashlib
import json
from cache import FileCache
from shapely.geometry import asShape
from shapely.geometry import Polygon
from shapely.geometry import Point

try:
    import cPickle as pickle
except ImportError:
    import pickle

class ReverseGeocoderShape(object):
    mapfile = ""
    maptype = "geojson"
    mapmd5 = ""
    index = []
    shapes = {}
    indexstep = 10

    def __init__(self,maptype,mapfile):
        self.maptype=maptype
        self.mapfile=mapfile
        mapfilehandler=open(self.mapfile)
        self.mapfilecontent=mapfilehandler.read()
        self.mapmd5 = hashlib.md5(self.mapfilecontent).hexdigest()
        mapfilehandler.close()
        self.loadmap()
        self.loadcache()
        self.loadindex()

    def loadmap(self):
        """ Load map content and transform it into a collection of Shapely polygons
        :return:
        """
        if self.maptype == "geojson":
            # read the geojson file
            json_map_data = json.loads(self.mapfilecontent)

            # iterate over all the polygons and store them
            for feature in json_map_data["features"]:
                feature_id=feature["properties"]["id"]
                self.shapes[feature_id]=asShape(feature["geometry"])

    def loadcache(self):
        """ Load cached results from a file
        :return:
        """
        cache = FileCache("reversegeocodeshape-"+self.mapmd5+".cache", 1000000, 62)
        cache.read_cache()

    def loadindex(self):
        """ Load a small index from a file, if not create one
        :return:
        """
        indexfile="reversegeocodeshape-"+self.mapmd5+".index"
        if os.path.isfile(indexfile):
            # Index exists, load it
            self.index = pickle.load(open(indexfile, "rb"))
        else:
            # Index does not exist create it
            self.createindex()
            pickle.dump(self.index,open(indexfile, "wb"))

    def createindex(self):
        print("Creating index")
        for lat in range(-90, 90, self.indexstep):
            for lng in range(-180, 180, self.indexstep):
                polygon = Polygon([(lng, lat), (lng+self.indexstep, lat), (lng, lat+self.indexstep),
                                   (lng+self.indexstep, lat+self.indexstep)])
                index_data = {"polygon": polygon, "keys": []}
                for key, shape in self.shapes.iteritems():
                    if shape.intersects(polygon):
                        index_data["keys"].append(key)
                if 0 < len(index_data["keys"]):
                    self.index.append(index_data)
        print("Index created")

    def reversegeocodeshape(self, point, key_list):
        for key in key_list:
            if self.shapes[key].contains(point):
                return key

    def reversegeocodeindex(self, lat, lng):
        point = Point(lng, lat)
        for shape in self.index:
            if shape["polygon"].contains(point):
                return self.reversegeocodeshape(point,shape["keys"])

    def reversegeocode(self,lat,lng):
        return self.reversegeocodeindex(lat,lng)





rev = ReverseGeocoderShape("geojson", "/home/pieter/git/heremaps/appserver/static/data/world2.geojson")
import csv
import datetime
with open("/home/pieter/git/heremaps/lookups/latlng-data.csv", 'rb') as csvfile:
    reader = csv.reader(csvfile)
    start = datetime.datetime.now()
    count = 0
    for row in reader:
        count += 1
        if count == 1:
            continue
        print(rev.reversegeocode(float(row[1]), float(row[0])))
        if count > 100:
            break

    stop = datetime.datetime.now()
    delta= stop-start
    print("Seconds: %s" % delta.seconds)

