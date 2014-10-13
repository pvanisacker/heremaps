#!/usr/bin/env python
import sys
import collections
import functools
import httplib2
import json

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from splunklib.results import ResultsReader
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
from tools.cache import FileCache

@Configuration()
class ReverseGeocodeCommand(StreamingCommand):

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

    prefix = Option(
        doc='''
        **Syntax:** **prefix=***customprefix*
        **Description:** Prefix for the fields that will contain the result''',
        require=False,default="regeo")

    app_id = ""
    app_code = ""
    cache = FileCache("reversegeocode.cache",1000000,62)

    def get_app_id(self):
        try:
            response = self.service.get("/servicesNS/nobody/heremaps/configs/conf-setup/heremaps")
            xml = response.body.read()
            root = et.fromstring(xml)
            self.app_id = root.findall(".//{http://dev.splunk.com/ns/rest}key[@name='app_id']")[0].text
            self.app_code = root.findall(".//{http://dev.splunk.com/ns/rest}key[@name='app_code']")[0].text
        except Exception as e:
            raise Exception("Could not get app_id and app_code, is the app set up correctly?",e)

    def _parseJSON(self,obj):
        if isinstance(obj, dict):
            newobj = {}
            for key, value in obj.iteritems():
                key = str(key)
                newobj[key] = self._parseJSON(value)
        elif isinstance(obj, list):
            newobj = []
            for value in obj:
                newobj.append(self._parseJSON(value))
        elif isinstance(obj, unicode):
            newobj = str(obj)
        else:
            newobj = obj
        return newobj

    def reverse_geocode(self,lat,lng):
        url = "http://reverse.geocoder.api.here.com/6.2/reversegeocode.json"+ \
              "?app_id=%s&app_code=%s&prox=%s,%s,10&" % (self.app_id, self.app_code, lat, lng) + \
              "gen=7&mode=retrieveAreas&maxresults=1&responseattributes=-ps,-mq,-mt,-mc,-pr&" + \
              "locationattributes=-mr,-mv,-ad,-ai"

        http = httplib2.Http()
        response, content = http.request(url,'GET')
        if response["status"] == "200":
            result = json.loads(content)
            # Make sure we don't get unicode strings
            result = self._parseJSON(result)
            try:
                return result["Response"]["View"][0]["Result"][0]["Location"]["Address"]
            except (KeyError, IndexError):
                self.logger.debug("Could not find any results for lat=%s and lng=%s",lat,lng)
                return {}
        else:
            self.logger.error("Got an unexpected for ulr %s response: %s", url, response)

    def add_fields(self, record, location):
        record[self.prefix + "_country"] = ""
        if "Country" in location:
            record[self.prefix + "_country"] = location["Country"]

        record[self.prefix + "_city"] = ""
        if "City" in location:
            record[self.prefix + "_city"] = location["City"]

        record[self.prefix + "_postalcode"] = ""
        if "PostalCode" in location:
            record[self.prefix + "_postalcode"] = location["PostalCode"]

        record[self.prefix + "_region"] = ""
        if "Region" in location:
            record[self.prefix + "_region"] = location["Region"]

        record[self.prefix + "_district"] = ""
        if "District" in location:
            record[self.prefix + "_district"] = location["District"]

        record[self.prefix + "_label"] = ""
        if "Label" in location:
            record[self.prefix + "_label"] = location["Label"]

        record[self.prefix + "_state"] = ""
        if "State" in location:
            record[self.prefix + "_state"] = location["State"]

        record[self.prefix + "_county"] = ""
        if "County" in location:
            record[self.prefix + "_county"] = location["County"]

    def stream(self, records):
        if self.app_id is "" or self.app_code is "":
            self.get_app_id()
        self.cache.read_cache()

        for record in records:
            lat = str(round(float(record[self.lat]), 5))
            lng = str(round(float(record[self.lng]), 5))

            cache_key = "%s,%s" % (lat, lng)
            location = self.cache.get(cache_key)
            if location is None:
                location = self.reverse_geocode(lat, lng)
                self.cache.set(cache_key,location)
            self.add_fields(record, location)

            yield record
        try:
            self.cache.write_cache()
        except:
            self.logger.error("Could not write cache file")



dispatch(ReverseGeocodeCommand, sys.argv, sys.stdin, sys.stdout, __name__)
