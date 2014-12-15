__author__ = 'pieter'

import unittest

from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from tools.reversegeocodershape import ReverseGeocoderShape


class ReverseGeocoderShapeTest(unittest.TestCase):
    def setUp(self):
        self.rev = ReverseGeocoderShape()
        self.rev.shapes["a"] = MultiPolygon([Polygon(((0, 0), (1, 0), (1, 1), (0, 1)))])
        self.rev.shapes["b"] = MultiPolygon([Polygon(((10, 20), (10, 21), (9, 23), (8, 7), (9, 15), (9.5, 16)))])
        self.rev.shapes["c"] = MultiPolygon(
            [Polygon(((20, 20), (20, 30), (30, 30), (30, 20)), [((21, 21), (21, 25), (25, 25), (25, 21))])])
        self.rev.shapes["d"] = MultiPolygon([Polygon(((21, 21), (21, 24), (24, 24), (24, 21)))])

    def tearDown(self):
        del self.rev

    def test_reversegeocodeshape_a(self):
        self.assertEqual("a", self.rev.reversegeocodeshape(Point(0.5, 0.5)))

    def test_reversegeocodeshape_a_corner(self):
        self.assertEqual("a", self.rev.reversegeocodeshape(Point(0, 0)))

    def test_reversegeocodeshape_a_on_edge(self):
        self.assertEqual("a", self.rev.reversegeocodeshape(Point(0.5, 0)))

    def test_reversegeocodeshape_b(self):
        self.assertEqual("b", self.rev.reversegeocodeshape(Point(9, 21)))

    def test_reversegeocodeshape_c(self):
        self.assertEqual("c", self.rev.reversegeocodeshape(Point(20.5, 20.5)))

    def test_reversegeocodeshape_c_inner_polygon(self):
        self.assertEqual(None, self.rev.reversegeocodeshape(Point(22, 24.5)))

    def test_reversegeocodeshape_d(self):
        self.assertEqual("d", self.rev.reversegeocodeshape(Point(22, 22)))

    def test_reversegeocodeshape_a_list_nok(self):
        self.assertEqual(None, self.rev.reversegeocodeshape(Point(0.5, 0.5), ["b", "c", "d"]))

    def test_reversegeocodeshape_a_list_ok(self):
        self.assertEqual("a", self.rev.reversegeocodeshape(Point(0.5, 0.5), ["b", "a", "d"]))
