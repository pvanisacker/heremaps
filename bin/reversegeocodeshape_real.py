import os
import sys
import json
from shapely.geometry import asShape
from shapely.geometry import Point
from tools.cache import FileCache
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
import hashlib

@Configuration()
class ReverseGeocodeShapeCommand(StreamingCommand):

    lat = Option(
        doc='''
        **Syntax:** **lat=***<fieldname>*
        **Description:** Name of the field that holds the latitude''',
        require=False,default="lat",validate=validators.Fieldname())

    lng = Option(
        doc='''
        **Syntax:** **lng=***<fieldname>*
        **Description:** Name of the field that holds the longitude''',
        require=False,default="lng", validate=validators.Fieldname())


    filetype = Option(
        doc='''
        **Syntax:** **filetype=***<filetype>*
        **Description:** Type of file: geojson or kml''',
        require=False,default="geojson")

    filename = Option(
        doc='''
        **Syntax:** **filename=***<filename>*
        **Description:** Name of the file''',
        require=False,default="world2.geojson")

    fieldname = Option(
        doc='''
        **Syntax:** **fieldname=***fieldname*
        **Description:** Name of the field that will contain the result''',
        require=False,default="key")

    shapes = {}

    def reversegeocodeshape(self, lat, lng):
        self.logger.info("shape %s" % lat)
        result = None
        point = Point(lng, lat)
        for key, shape in self.shapes.iteritems():
            if shape.contains(point):
                result = key

        return result

    def stream(self, records):
        md5sum_map = ""
        # read file and store it into the shape collection
        if self.filetype == "geojson":
            # read the geojson file
            json_map_file=open(os.environ['SPLUNK_HOME']+"/etc/apps/heremaps/appserver/static/data/"+self.filename)
            json_map_content=json_map_file.read()
            md5sum_map=hashlib.md5(json_map_content).hexdigest()
            json_map_data=json.loads(json_map_content)
            json_map_file.close()

            # iterate over all the polygons and store them
            for feature in json_map_data["features"]:
                feature_id=feature["properties"]["id"]
                self.shapes[feature_id]=asShape(feature["geometry"])
        if self.filetype=="kml":
            # TODO implement this stuff
            # read the kml file

            # iterate over all the polygons and store them
            pass

        cache = FileCache("reversegeocodeshape-"+md5sum_map+".cache", 1000000, 62)
        cache.read_cache()

        # iterate over records
        for record in records:
            lat = round(float(record[self.lat]), 5)
            lng = round(float(record[self.lng]), 5)
            cache_key = "%s,%s" % (lat, lng)
            try:
                key = cache.get(cache_key)
            except KeyError as e:
                key = self.reversegeocodeshape(lat, lng)

            cache.set(cache_key, key)
            record[self.fieldname] = key
            yield record

        try:
            cache.write_cache()
        except:
            self.logger.error("Could not write cache file")

dispatch(ReverseGeocodeShapeCommand, sys.argv, sys.stdin, sys.stdout, __name__)