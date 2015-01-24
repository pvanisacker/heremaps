__author__ = 'pieter'

import unittest
import os

from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from tools.reversegeocodershape import ReverseGeocoderShape


class ReverseGeocoderShapeMapTest(unittest.TestCase):
    def setUp(self):
        self.rev = ReverseGeocoderShape()
        self.basepath = "."
        self.filetype = "geojson"

    def tearDown(self):
        del self.rev

    def test_map_world2(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "world2.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "BE")
