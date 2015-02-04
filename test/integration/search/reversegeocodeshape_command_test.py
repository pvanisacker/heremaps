__author__ = 'pieter.van.isacker'

import unittest
from .util import create_connection
from .util import return_first_result


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

    """
        Start testing for the different continents
    """

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
        self.assertEqual(result["key"], "BEL")

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
        self.assertEqual(result["key"], "AUS")

    def test_reverse_geocode_shape_command_custom_map_continent_south_america(self):
        search = "search * | head 1 | eval lat=-33 | eval lng=-66 | " + \
                 "reversegeocodeshape filetype=geojson filename=continents/south-america.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "-33")
        self.assertEqual(result["lng"], "-66")
        self.assertEqual(result["key"], "ARG")

    """
        Start testing for the different countries
    """
    def test_map_country_be(self):
        search = "search * | head 1 | eval lat=51 | eval lng=3 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/be.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "3")
        self.assertEqual(result["key"], "West Flanders")

    def test_map_country_br(self):
        search = "search * | head 1 | eval lat=-8 | eval lng=-63 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/br.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "-8")
        self.assertEqual(result["lng"], "-63")
        self.assertEqual(result["key"], "Amazonas")

    def test_map_country_ca(self):
        search = "search * | head 1 | eval lat=53 | eval lng=-113 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/ca.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "53")
        self.assertEqual(result["lng"], "-113")
        self.assertEqual(result["key"], "Alberta")

    def test_map_country_cn(self):
        search = "search * | head 1 | eval lat=34 | eval lng=108 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/cn.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "34")
        self.assertEqual(result["lng"], "108")
        self.assertEqual(result["key"], "Shaanxi")

    def test_map_country_de(self):
        search = "search * | head 1 | eval lat=52 | eval lng=13 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/de.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "52")
        self.assertEqual(result["lng"], "13")
        self.assertEqual(result["key"], "Brandenburg")

    def test_map_country_es(self):
        search = "search * | head 1 | eval lat=41 | eval lng=-1 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/es.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "41")
        self.assertEqual(result["lng"], "-1")
        self.assertEqual(result["key"], "Teruel")

    def test_map_country_fr(self):
        search = "search * | head 1 | eval lat=49 | eval lng=0 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/fr.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "49")
        self.assertEqual(result["lng"], "0")
        self.assertEqual(result["key"], "Calvados")

    def test_map_country_in(self):
        search = "search * | head 1 | eval lat=18 | eval lng=75 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/in.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "18")
        self.assertEqual(result["lng"], "75")
        self.assertEqual(result["key"], "Maharashtra")

    def test_map_country_it(self):
        search = "search * | head 1 | eval lat=42 | eval lng=12 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/it.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "42")
        self.assertEqual(result["lng"], "12")
        self.assertEqual(result["key"], "Roma")

    def test_map_country_ru(self):
        search = "search * | head 1 | eval lat=55 | eval lng=37 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/ru.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "55")
        self.assertEqual(result["lng"], "37")
        self.assertEqual(result["key"], "Kaluga")

    def test_map_country_uk(self):
        search = "search * | head 1 | eval lat=51 | eval lng=0 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/uk.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "51")
        self.assertEqual(result["lng"], "0")
        self.assertEqual(result["key"], "East Sussex")

    def test_map_country_us(self):
        search = "search * | head 1 | eval lat=33 | eval lng=-84 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/us.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "33")
        self.assertEqual(result["lng"], "-84")
        self.assertEqual(result["key"], "GA")

    """
    def test_map_country_us_counties(self):
        map_file = os.path.join(self.basepath, "appserver", "static", "data", "countries/us_counties.geojson")
        self.rev.load_map_file(self.filetype, map_file)
        self.load_index()
        key = self.rev.reversegeocode(33, -84)
        self.assertEqual(key, "13207")
    """

    def test_map_country_us_simplified(self):
        search = "search * | head 1 | eval lat=33 | eval lng=-84 | " + \
                 "reversegeocodeshape filetype=geojson filename=countries/us_simplified.geojson | fields lat,lng,key"
        result = return_first_result(self.splunkservice, search)
        self.assertIsNotNone(result)
        self.assertEqual(result["lat"], "33")
        self.assertEqual(result["lng"], "-84")
        self.assertEqual(result["key"], "GA")
