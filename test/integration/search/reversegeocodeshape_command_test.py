__author__ = 'pieter.van.isacker'

import unittest
from .util import *


class ReverseGeocodeShapeCommandTest(unittest.TestCase):
    def setUp(self):
        self.splunkservice = create_connection()

    def test_reverse_geocode_shape_command_default(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | " + \
                 "reversegeocodeshape | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
        self.assertEqual(result["key"], "BE")

    def test_reverse_geocode_shape_command_custom_field(self):
        search = "search * | head 1 | eval latitude=51 | eval longitude=3 | " + \
                 "reversegeocodeshape lat=latitude lng=longitude | fields latitude,longitude,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["latitude"], "51")
        self.assertEqual(result["longitude"], "3")
        self.assertEqual(result["key"], "BE")

    def test_reverse_geocode_shape_command_custom_key(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | " + \
                 "reversegeocodeshape fieldname=mykey| fields lat,lng,mykey"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
        self.assertEqual(result["mykey"], "BE")

    def test_reverse_geocode_shape_command_custom_map(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | " + \
                 "reversegeocodeshape filetype=geojson filename=world2.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
        self.assertEqual(result["key"], "BE")

    def test_reverse_geocode_shape_command_custom_map_custom(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | " + \
                 "reversegeocodeshape filetype=geojson filename=custom.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
        self.assertEqual(result["key"], "area1")

    def test_reverse_geocode_shape_command_custom_map_hexagon_regeo_2(self):
        search = "search * | head 1 | eval lat=51.1 | eval lng=3.1 | " + \
                 "reversegeocodeshape filetype=geojson filename=hexagonmap_regeo_2.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51.1")
        self.assertEqual(result["lng"], "3.1")
        self.assertEqual(result["key"], "3350")

    def test_reverse_geocode_shape_command_custom_map_hexagon_regeo_3(self):
        search = "search * | head 1 | eval lat=51.1 | eval lng=3.1 | " + \
                 "reversegeocodeshape filetype=geojson filename=hexagonmap_regeo_3.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51.1")
        self.assertEqual(result["lng"], "3.1")
        self.assertEqual(result["key"], "1634")

    def test_reverse_geocode_shape_command_custom_map_square_2(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | " + \
                 "reversegeocodeshape filetype=geojson filename=squaremap_2.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
        self.assertEqual(result["key"], "12691")

    def test_reverse_geocode_shape_command_custom_map_square_4(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | " + \
                 "reversegeocodeshape filetype=geojson filename=squaremap_4.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
        self.assertEqual(result["key"], "3195")

    def test_reverse_geocode_shape_command_custom_map_world3(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | " + \
                 "reversegeocodeshape filetype=geojson filename=world3.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
        self.assertEqual(result["key"], "BEL")

    def test_reverse_geocode_shape_command_custom_map_continent_africa(self):
        search = "search * | head 1 | eval lat=11 | eval lng=17 | " + \
                 "reversegeocodeshape filetype=geojson filename=continents/africa.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "11")
        self.assertEqual(result["lng"], "17")
        self.assertEqual(result["key"], "TCD")

    def test_reverse_geocode_shape_command_custom_map_continent_asia(self):
        search = "search * | head 1 | eval lat=19 | eval lng=73 | " + \
                 "reversegeocodeshape filetype=geojson filename=continents/asia.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "19")
        self.assertEqual(result["lng"], "73")
        self.assertEqual(result["key"], "IND")

    def test_reverse_geocode_shape_command_custom_map_continent_europe(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | " + \
                 "reversegeocodeshape filetype=geojson filename=continents/europe.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
        self.assertEqual(result["key"], "BE")

    def test_reverse_geocode_shape_command_custom_map_continent_north_america(self):
        search = "search * | head 1 | eval lat=50 | eval lng=-104 | " + \
                 "reversegeocodeshape filetype=geojson filename=continents/north-america.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "50")
        self.assertEqual(result["lng"], "-104")
        self.assertEqual(result["key"], "CAN")

    def test_reverse_geocode_shape_command_custom_map_continent_oceania(self):
        search = "search * | head 1 | eval lat=-33 | eval lng=150 | " + \
                 "reversegeocodeshape filetype=geojson filename=continents/oceania.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "-33")
        self.assertEqual(result["lng"], "150")
        self.assertEqual(result["key"], "BE")

    def test_reverse_geocode_shape_command_custom_map_continent_south_america(self):
        search = "search * | head 1 | eval lat=-33 | eval lng=-66 | " + \
                 "reversegeocodeshape filetype=geojson filename=continents/south-america.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "-33")
        self.assertEqual(result["lng"], "-66")
        self.assertEqual(result["key"], "BE")
