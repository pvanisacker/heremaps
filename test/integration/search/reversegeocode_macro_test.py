__author__ = 'pieter.van.isacker'

import unittest
from .util import *


class ReverseGeocodeMacroTest(unittest.TestCase):
    def setUp(self):
        self.splunkservice = create_connection()

    def test_reverse_geocode_macro_default(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | `reversegeocode` | fields lat,lng,regeo*"

        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["regeo_country"], "BEL")
        self.assertEqual(result["regeo_country_iso3166_2"], "BE")
        self.assertEqual(result["regeo_country_latitude"], "50.503887")
        self.assertEqual(result["regeo_country_longitude"], "4.469936")
        self.assertEqual(result["regeo_country_name"], "Belgium")
        self.assertEqual(result["regeo_state"], "Vlaanderen")
        self.assertEqual(result["regeo_county"], "West-Vlaanderen")
        self.assertEqual(result["regeo_city"], "Kortemark")
        self.assertEqual(result["regeo_postalcode"], "8610")
        self.assertEqual(result["regeo_label"], 'Kortemark, Vlaanderen, Belgi\xc3\xab')
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
