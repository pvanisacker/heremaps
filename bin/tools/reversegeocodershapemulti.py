__author__ = 'pieter'
import os
import hashlib
import json
import multiprocessing
from multiprocessing import Pool

from shapely.geometry import asShape
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import mapping

try:
    import cPickle as pickle
except ImportError:
    import pickle


def check_intersects(data):
    polygon = Polygon(((data["lng"], data["lat"]),
                       (data["lng"] + data["step"], data["lat"]),
                       (data["lng"] + data["step"], data["lat"] + data["step"]),
                       (data["lng"], data["lat"] + data["step"])))
    if data["shape"].intersects(polygon):
        return {"lat": data["lat"], "lng": data["lng"], "key": data["key"], "poly": polygon}


def reversegeocodeshape_check_intersects(key, shapegeojson, point):
    shape = asShape(shapegeojson)
    if shape.intersects(point):
        return key


class ReverseGeocoderShapeMulti(object):
    def __init__(self):
        self.shapes = {}
        self.map_file_content = None
        self.map_type = None
        self.map_md5 = None
        self.map_loaded = False
        self.index_loaded = False
        self.index = []
        self.indexstep = 5

    def load_map_file(self, map_type, map_file):
        self.map_file = map_file
        self.load_map_handler(map_type, open(self.map_file, "rb"))

    def load_map_handler(self, map_type, maphandler):
        """ Load map content and transform it into a collection of Shapely polygons
        :return:
        """
        self.map_type = map_type
        self.map_file_content = maphandler.read()
        self.map_md5 = hashlib.md5(self.map_file_content).hexdigest()
        maphandler.close()
        if self.map_type == "geojson":
            self.load_map_geojson()
        if self.map_type == "kml":
            self.load_map_kml()

        self.map_loaded = True

    def load_map_geojson(self):
        # read the geojson file
        self.json_map_data = json.loads(self.map_file_content)

        # iterate over all the polygons and store them
        for feature in self.json_map_data["features"]:
            if "properties" in feature and "id" in feature["properties"] and len(
                    feature["properties"]["id"].strip()) > 0:
                if "geometry" in feature and "type" in feature["geometry"] and feature["geometry"]["type"] == "MultiPolygon":
                    feature_id = feature["properties"]["id"]
                    self.shapes[feature_id] = asShape(feature["geometry"])

    def load_map_kml(self):
        raise NotImplementedError()

    def load_index(self, basedir):
        self.load_index_file(os.path.join(basedir, "reversegeocodeshape-" + self.map_md5 + ".index"))

    def load_index_file(self, indexfile):
        try:
            if self.json_map_data["crs"]["properties"]["needsindex"] is False:
                return
        except KeyError:
            pass
        if os.path.isfile(indexfile):
            # Index exists, load it
            self.index = pickle.load(open(indexfile, "rb"))
        else:
            # Index does not exist create it
            self.createindex()
            pickle.dump(self.index, open(indexfile, "wb"))
        self.index_loaded = True

    def createindex(self):
        items = []
        for lat in range(-90, 90, self.indexstep):
            for lng in range(-180, 180, self.indexstep):
                for key, shape in self.shapes.iteritems():
                    items.append({"key": key, "shape": shape, "lat": lat, "lng": lng, "step": self.indexstep})

        processing_count = multiprocessing.cpu_count()
        pool = Pool(processing_count)

        result = pool.map(check_intersects, items)
        pool.close()
        pool.join()

        # remove empty results
        result = filter(lambda x: x is not None, result)

        # transform results into dict
        temp = {}
        for res in result:
            poly = str(res["lat"])+","+str(res["lng"])
            if poly in temp:
                # update value in dict
                temp[poly]["keys"].append(res["key"])
            else:
                # add to dict
                temp[poly] = {"polygon": res["poly"], "keys": [res["key"]]}

        # tranform results into array
        for key, value in temp.iteritems():
            self.index.append(value)

    def reversegeocodeshape(self, point, keys=None):
        processing_count = multiprocessing.cpu_count()
        pool = Pool(processing_count)
        key_result = []

        def handleresult(key):
            if key is not None:
                key_result.append(key)

        for key, shape in self.shapes.iteritems():
            if keys is not None and key not in keys:
                continue
            else:
                if len(key_result) == 0:
                    shapejson = mapping(shape)
                    pool.apply_async(reversegeocodeshape_check_intersects, args=(key, shapejson, point), callback = handleresult)

        pool.close()
        pool.join()
        result = None
        if len(key_result) > 0:
            result = key_result[0]
        return result

    def reversegeocodeindex(self, point):
        for shape in self.index:
            if shape["polygon"].intersects(point):
                return self.reversegeocodeshape(point, shape["keys"])

    def reversegeocode(self, lat, lng):
        point = Point(lng, lat)
        if self.index_loaded:
            return self.reversegeocodeindex(point)
        else:
            return self.reversegeocodeshape(point)
