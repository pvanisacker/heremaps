import os
import sys

from tools.cache import FileCache

# Use the multiprocessing/multi core version
from tools.reversegeocodershapemulti import ReverseGeocoderShapeMulti as ReverseGeocoderShape

# Use the single core version
# from tools.reversegeocodershape import ReverseGeocoderShape

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators


@Configuration()
class ReverseGeocodeShapeCommand(StreamingCommand):
    lat = Option(
        doc='''
        **Syntax:** **lat=***<fieldname>*
        **Description:** Name of the field that holds the latitude''',
        require=False, default="lat", validate=validators.Fieldname())

    lng = Option(
        doc='''
        **Syntax:** **lng=***<fieldname>*
        **Description:** Name of the field that holds the longitude''',
        require=False, default="lng", validate=validators.Fieldname())

    filetype = Option(
        doc='''
        **Syntax:** **filetype=***<filetype>*
        **Description:** Type of file: geojson or kml''',
        require=False, default="geojson")

    filename = Option(
        doc='''
        **Syntax:** **filename=***<filename>*
        **Description:** Name of the file''',
        require=False, default="world2.geojson")

    fieldname = Option(
        doc='''
        **Syntax:** **fieldname=***fieldname*
        **Description:** Name of the field that will contain the result''',
        require=False, default="key")

    def stream(self, records):
        basepath = os.path.join(os.environ['SPLUNK_HOME'], "etc", "apps", "heremaps")

        rev = ReverseGeocoderShape()
        map_file = os.path.join(basepath, "appserver", "static", "data", self.filename)
        rev.load_map_file(self.filetype, map_file)
        self.logger.info("Loaded map file %s" % self.filename)

        # Load map index file, this speeds up the command a lot
        index_file = os.path.join(basepath, "bin", "lib")
        rev.load_index(index_file)
        self.logger.info("Loaded map index %s" % index_file)

        # Load cached results
        cache_file = os.path.join(basepath, "bin", "lib", "reversegeocodeshape-" + rev.map_md5 + ".cache")
        self.cache = FileCache(1000000, 62)
        self.cache.read_cache_file(cache_file)
        self.logger.info("Loaded cached results %s" % cache_file)

        # iterate over records
        for record in records:
            lat = round(float(record[self.lat]), 5)
            lng = round(float(record[self.lng]), 5)
            cache_key = "%s,%s" % (lat, lng)
            try:
                key = self.cache.get(cache_key)
            except KeyError:
                key = rev.reversegeocode(lat, lng)

            self.cache.set(cache_key, key)
            record[self.fieldname] = key
            yield record

        try:
            self.cache.write_cache_file(cache_file)
        except:
            self.logger.error("Could not write cache file")
        rev.stop()


dispatch(ReverseGeocodeShapeCommand, sys.argv, sys.stdin, sys.stdout, __name__)
