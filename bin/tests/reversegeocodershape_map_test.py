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

    def test_map_custom(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "custom.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "area1")

    def test_map_hexagonmap_display_2(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "hexagonmap_display_2.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key,"3350")

    def test_map_hexagonmap_display_3(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "hexagonmap_display_3.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertIsNone(key)

    def test_map_hexagonmap_regeo_2(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "hexagonmap_regeo_2.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "3350")

    def test_map_hexagonmap_regeo_3(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "hexagonmap_regeo_3.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "1514")

    def test_map_squaremap_2(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "squaremap_2.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "12691")

    def test_map_squaremap_4(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "squaremap_4.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "3195")

    def test_map_world2(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "world2.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "BE")

    def test_map_world3(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "world3.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "BEL")
