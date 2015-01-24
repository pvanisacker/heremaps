__author__ = 'pieter'

import unittest

from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from tools.reversegeocodershape import ReverseGeocoderShape


class ReverseGeocoderShapeIndexTest(unittest.TestCase):
    def setUp(self):
        self.rev = ReverseGeocoderShape()
        self.rev.shapes["a"] = MultiPolygon([Polygon(((0, 0), (1, 0), (1, 1), (0, 1)))])
        self.rev.shapes["b"] = MultiPolygon([Polygon(((10, 20), (10, 21), (9, 23), (8, 7), (9, 15), (9.5, 16)))])
        self.rev.shapes["c"] = MultiPolygon(
            [Polygon(((20, 20), (20, 30), (30, 30), (30, 20)), [((21, 21), (21, 25), (25, 25), (25, 21))])])
        self.rev.shapes["d"] = MultiPolygon([Polygon(((21, 21), (21, 24), (24, 24), (24, 21)))])
        self.rev.createindex()

    def tearDown(self):
        del self.rev

    def test_create_index(self):
        self.assertEqual(26, len(self.rev.index))
        self.assertEqual(["a"], self.rev.index[0]["keys"])
        self.assertEqual(["a"], self.rev.index[2]["keys"])
        self.assertEqual(["b"], self.rev.index[4]["keys"])
        self.assertEqual(["b"], self.rev.index[6]["keys"])
        self.assertEqual(["c"], self.rev.index[8]["keys"])
        self.assertEqual(["c", "d"], self.rev.index[15]["keys"])

    def test_reversegeocodeindex(self):
        self.assertEqual("a", self.rev.reversegeocodeindex(Point(0.5, 0.5)))
