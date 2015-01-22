__author__ = 'pieter.van.isacker'

import unittest
from .util import *

class ReverseGeocodeCommandTest(unittest.TestCase):
    def setUp(self):
        self.splunkservice = create_connection()

    def test_reverse_geocode_command_default(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3| reversegeocode | fields lat,lng,regeo_*"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["regeo_country"], "BEL")
        self.assertEqual(result["regeo_state"], "Vlaanderen")
        self.assertEqual(result["regeo_county"], "West-Vlaanderen")
        self.assertEqual(result["regeo_city"], "Kortemark")
        self.assertEqual(result["regeo_postalcode"], "8610")
        self.assertEqual(result["regeo_label"], 'Kortemark, Vlaanderen, Belgi\xc3\xab')
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")

    def test_reverse_geocode_command_custom_lat_lng(self):
        search = "search * | head 1 | eval latitude=51 | eval longitude=6 | reversegeocode lat=latitude,lng=longitude | fields latitude,longitude,regeo_*"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["regeo_country"], "DEU")
        self.assertEqual(result["regeo_state"], "Nordrhein-Westfalen")
        self.assertEqual(result["regeo_county"], "Heinsberg")
        self.assertEqual(result["regeo_city"], "Gangelt")
        self.assertEqual(result["regeo_postalcode"], "52538")
        self.assertEqual(result["regeo_label"], 'Gangelt, Nordrhein-Westfalen, Deutschland')
        self.assertEqual(result["latitude"], "51")
        self.assertEqual(result["longitude"], "6")

    def test_reverse_geocode_command_custom_prefix(self):
        search = "search * | head 1 | eval lat=51 | eval lng=6 | reversegeocode prefix=myprefix | fields lat,lng,myprefix_*"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["myprefix_country"], "DEU")
        self.assertEqual(result["myprefix_state"], "Nordrhein-Westfalen")
        self.assertEqual(result["myprefix_county"], "Heinsberg")
        self.assertEqual(result["myprefix_city"], "Gangelt")
        self.assertEqual(result["myprefix_postalcode"], "52538")
        self.assertEqual(result["myprefix_label"], 'Gangelt, Nordrhein-Westfalen, Deutschland')
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "6")
