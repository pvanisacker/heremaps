import unittest
import os

from tools.reversegeocodershapemulti import ReverseGeocoderShapeMulti as ReverseGeocoderShape


class ReverseGeocoderShapeMapTest(unittest.TestCase):
    def setUp(self):
        self.rev = ReverseGeocoderShape()
        self.basepath = "."
        self.filetype = "geojson"

    def tearDown(self):
        self.rev.stop()
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
        self.assertEqual(key, "3350")

    """
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
    """
    """
        Start testing for the different continents
    """
    """
    def test_map_continent_africa(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "continents/africa.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(17, 9)
        self.assertEqual(key, "NER")

    def test_map_continent_asia(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "continents/asia.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(19, 73)
        self.assertEqual(key, "IND")

    def test_map_continent_europe(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "continents/europe.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "BEL")

    def test_map_continent_north_america(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "continents/north-america.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(45, -75)
        self.assertEqual(key, "CAN")

    def test_map_continent_oceania(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "continents/oceania.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(-33, 150)
        self.assertEqual(key, "AUS")

    def test_map_continent_south_america(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "continents/south-america.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(-31, -64)
        self.assertEqual(key, "ARG")
    """
    """
        Start testing for the different countries
    """
    """
    def test_map_country_be(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/be.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 3)
        self.assertEqual(key, "West Flanders")

    def test_map_country_br(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/br.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(-8, -63)
        self.assertEqual(key, "Amazonas")

    def test_map_country_ca(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/ca.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(53, -113)
        self.assertEqual(key, "Alberta")

    def test_map_country_cn(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/cn.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(34, 108)
        self.assertEqual(key, "Shaanxi")

    def test_map_country_de(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/de.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(52, 13)
        self.assertEqual(key, "Brandenburg")

    def test_map_country_es(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/es.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(41, -1)
        self.assertEqual(key, "Teruel")

    def test_map_country_fr(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/fr.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(49, 0)
        self.assertEqual(key, "Calvados")

    def test_map_country_in(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/in.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(18, 75)
        self.assertEqual(key, "Maharashtra")

    def test_map_country_it(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/it.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(42, 12)
        self.assertEqual(key, "Roma")

    def test_map_country_ru(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/ru.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(55, 37)
        self.assertEqual(key, "Kaluga")

    def test_map_country_uk(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/uk.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(51, 0)
        self.assertEqual(key, "East Sussex")

    def test_map_country_us(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/us.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(33, -84)
        self.assertEqual(key, "GA")

    def test_map_country_us_counties(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/us_counties.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(33, -84)
        self.assertEqual(key, "13207")

    def test_map_country_us_simplified(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/us_simplified.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        key = self.rev.reversegeocode(33, -84)
        self.assertEqual(key, "GA")
    """
