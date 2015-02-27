import unittest

from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from tools.reversegeocodershapemulti import ReverseGeocoderShapeMulti as ReverseGeocoderShape


class ReverseGeocoderShapeIndexTest(unittest.TestCase):
    def setUp(self):
        self.rev = ReverseGeocoderShape()
        self.rev.shapes["a"] = MultiPolygon([Polygon(((0, 0), (1, 0), (1, 1), (0, 1)))])
        self.rev.shapes["b"] = MultiPolygon([Polygon(((10, 20), (10, 21), (9, 23), (8, 7), (9, 15), (9.5, 16)))])
        self.rev.shapes["c"] = MultiPolygon(
            [Polygon(((20, 20), (20, 30), (30, 30), (30, 20)), [((21, 21), (21, 25), (25, 25), (25, 21))])])
        self.rev.shapes["d"] = MultiPolygon([Polygon(((21, 21), (21, 24), (24, 24), (24, 21)))])
        self.rev.shapes["e"] = MultiPolygon([Polygon(((1, 0), (2, 0), (2, 1), (1, 1)))])
        self.rev.createindex()

    def tearDown(self):
        self.rev.stop()
        del self.rev

    def test_create_index(self):
        self.assertEqual(26, len(self.rev.index))
        self.assertEqual(["c"], self.rev.index[0]["keys"])
        self.assertEqual(["a", "e"], self.rev.index[1]["keys"])
        self.assertEqual(["c"], self.rev.index[2]["keys"])
        self.assertEqual(["c"], self.rev.index[3]["keys"])
        self.assertEqual(["c"], self.rev.index[4]["keys"])
        self.assertEqual(["c"], self.rev.index[6]["keys"])
        self.assertEqual(["b"], self.rev.index[8]["keys"])
        self.assertEqual(["c"], self.rev.index[15]["keys"])

    def test_reversegeocodeindex_a(self):
        self.assertEqual("a", self.rev.reversegeocodeindex(Point(0.5, 0.5)))

    def test_reversegeocodeindex_a_corner(self):
        self.assertEqual("a", self.rev.reversegeocodeindex(Point(0, 0)))

    def test_reversegeocodeindex_a_corner1(self):
        # This is not really nice, but the behaviour is dependant on the multiprocessing part
        # Which is hard to predict
        self.assertIn(self.rev.reversegeocodeindex(Point(1, 0)), ["a", "e"])

    def test_reversegeocodeindex_b(self):
        self.assertEqual("b", self.rev.reversegeocodeindex(Point(9.5, 22)))

    def test_reversegeocodeindex_c(self):
        self.assertEqual("c", self.rev.reversegeocodeindex(Point(25, 25)))

    def test_reversegeocodeindex_d(self):
        self.assertEqual("d", self.rev.reversegeocodeindex(Point(22, 23)))

    def test_reversegeocodeindex_e(self):
        self.assertEqual("e", self.rev.reversegeocodeindex(Point(1.5, 0.5)))

    def test_reversegeocodeindex_none(self):
        self.assertEqual(None, self.rev.reversegeocodeindex(Point(-1, -1)))
