#!/usr/bin/env python
import sys
import collections
import functools
import httplib2
import json

try:
    import xml.etree.cElementTree as et
except:
    import xml.etree.ElementTree as et

from splunklib.results import ResultsReader
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
       self.func = func
       self.cache = {}
   def __call__(self, *args):
       if not isinstance(args, collections.Hashable):
          # uncacheable. a list, for instance.
          # better to not cache than blow up.
          return self.func(*args)
       if args in self.cache:
          return self.cache[args]
       else:
          value = self.func(*args)
          self.cache[args] = value
          return value
   def __repr__(self):
       '''Return the function's docstring.'''
       return self.func.__doc__
   def __get__(self, obj, objtype):
       '''Support instance methods.'''
       return functools.partial(self.__call__, obj)

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

    def get_app_id(self):
        try:
            response = self.service.get("/servicesNS/nobody/heremaps/configs/conf-setup/heremaps")
            xml = response.body.read()
            root = et.fromstring(xml)
            self.app_id = root.findall(".//{http://dev.splunk.com/ns/rest}key[@name='app_id']")[0].text
            self.app_code = root.findall(".//{http://dev.splunk.com/ns/rest}key[@name='app_code']")[0].text
        except Exception as e:
            raise Exception("Could not get app_id and app_code, is the app set up correctly?",e)

    @memoized
    def reverse_geocode(self,lat,lng):
        url = "http://reverse.geocoder.api.here.com/6.2/reversegeocode.json"+ \
              "?app_id=%s&app_code=%s&prox=%s,%s,10&" % (self.app_id, self.app_code, lat, lng) + \
              "gen=7&mode=retrieveAreas&maxresults=1&responseattributes=-ps,-mq,-mt,-mc,-pr&" + \
              "locationattributes=-mr,-mv,-ad,-ai"

        http = httplib2.Http()
        response, content = http.request(url,'GET')
        if response["status"]=="200":
            result = json.loads(content)
            try:
                return result["Response"]["View"][0]["Result"][0]["Location"]["Address"]
            except (KeyError, IndexError):
                self.logger.debug("Could not find any results for lat=%s and lng=%s",lat,lng)
                return {}
        else:
            self.logger.error("Got an unexpected for ulr %s response: %s",url,response)

    def add_fields(self, record, location):
        record[self.prefix + "_country"] = ""
        if "Country" in location:
            record[self.prefix + "_country"] = location["Country"].encode('ascii', 'replace')

        record[self.prefix + "_city"] = ""
        if "City" in location:
            record[self.prefix + "_city"] = location["City"].encode('ascii', 'replace')

        record[self.prefix + "_postalcode"] = ""
        if "PostalCode" in location:
            record[self.prefix + "_postalcode"] = location["PostalCode"].encode('ascii', 'replace')

        record[self.prefix + "_region"] = ""
        if "Region" in location:
            record[self.prefix + "_region"] = location["Region"].encode('ascii', 'replace')

        record[self.prefix + "_district"] = ""
        if "District" in location:
            record[self.prefix + "_district"] = location["District"].encode('ascii', 'replace')

        record[self.prefix + "_label"] = ""
        if "Label" in location:
            record[self.prefix + "_label"] = location["Label"].encode('ascii', 'replace')

        record[self.prefix + "_state"] = ""
        if "State" in location:
            record[self.prefix + "_state"] = location["State"].encode('ascii', 'replace')

        record[self.prefix + "_county"] = ""
        if "County" in location:
            record[self.prefix + "_county"] = location["County"].encode('ascii', 'replace')

    def stream(self, records):
        if self.app_id is "" or self.app_code is "":
            self.get_app_id()

        for record in records:
            lat = str(round(float(record[self.lat]),5))
            lng = str(round(float(record[self.lng]),5))
            location = self.reverse_geocode(lat, lng)
            self.add_fields(record, location)

            yield record

dispatch(ReverseGeocodeCommand, sys.argv, sys.stdin, sys.stdout, __name__)
