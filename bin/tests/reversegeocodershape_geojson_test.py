import unittest

from tools.reversegeocodershape import ReverseGeocoderShape


class ReverseGeocoderShapeGeoJsonTest(unittest.TestCase):
    def test_load_geojson_correct(self):
        map_data = """
                {"type": "FeatureCollection",
                    "features": [
                        {"type": "Feature","properties": {"id":"1"},"geometry": {"type": "MultiPolygon",
                            "coordinates": [[[[4,46],[4,48],[7,48],[7,46],[4,46]]]]}},
                        {"type": "Feature","properties": {"id":"2"},"geometry": {"type": "MultiPolygon",
                            "coordinates": [[[[7,49],[7,50],[10,50],[10,49],[7,49]]]]}}
                    ]
                }
        """
        rev = ReverseGeocoderShape()
        rev.map_file_content = map_data
        rev.load_map_geojson()
        self.assertEqual(2, len(rev.shapes))

    def test_load_geojson_properties_missing(self):
        """ Test if no items are added if the properties are missing
        :return:
        """
        map_data = """
                {"type": "FeatureCollection",
                    "features": [
                        {"type": "Feature","geometry": {"type": "MultiPolygon",
                            "coordinates": [[[[4,46],[4,48],[7,48],[7,46],[4,46]]]]}},
                        {"type": "Feature","geometry": {"type": "MultiPolygon",
                            "coordinates": [[[[7,49],[7,50],[10,50],[10,49],[7,49]]]]}}
                    ]
                }
        """
        rev = ReverseGeocoderShape()
        rev.map_file_content = map_data
        rev.load_map_geojson()
        self.assertEqual(0, len(rev.shapes))

    def test_load_geojson_properties_empty(self):
        """ Test if no items are added if the properties are empty
        :return:
        """
        map_data = """
                {"type": "FeatureCollection",
                    "features": [
                        {"type": "Feature","properties":{},"geometry": {"type": "MultiPolygon",
                            "coordinates": [[[[4,46],[4,48],[7,48],[7,46],[4,46]]]]}},
                        {"type": "Feature","properties":{},"geometry": {"type": "MultiPolygon",
                            "coordinates": [[[[7,49],[7,50],[10,50],[10,49],[7,49]]]]}}
                    ]
                }
        """
        rev = ReverseGeocoderShape()
        rev.map_file_content = map_data
        rev.load_map_geojson()
        self.assertEqual(0, len(rev.shapes))

    def test_load_geojson_id_empty(self):
        """ Test if no items are added if the id is empty
        :return:
        """
        map_data = """
                {"type": "FeatureCollection",
                    "features": [
                        {"type": "Feature","properties":{"id":"   "},"geometry": {"type": "MultiPolygon",
                            "coordinates": [[[[4,46],[4,48],[7,48],[7,46],[4,46]]]]}},
                        {"type": "Feature","properties":{"id":"   "},"geometry": {"type": "MultiPolygon",
                            "coordinates": [[[[7,49],[7,50],[10,50],[10,49],[7,49]]]]}}
                    ]
                }
        """
        rev = ReverseGeocoderShape()
        rev.map_file_content = map_data
        rev.load_map_geojson()
        self.assertEqual(0, len(rev.shapes))

    def test_load_geojson_not_multipolygon(self):
        map_data = """
                {"type": "FeatureCollection",
                    "features": [
                        {"type": "Feature","properties":{"id":"1"},"geometry": {"type": "Polygon",
                            "coordinates": [[[4,46],[4,48],[7,48],[7,46],[4,46]]]}},
                        {"type": "Feature","properties":{"id":"2"},"geometry": {"type": "Polygon",
                            "coordinates": [[[7,49],[7,50],[10,50],[10,49],[7,49]]]}}
                    ]
                }
        """
        rev = ReverseGeocoderShape()
        rev.map_file_content = map_data
        rev.load_map_geojson()
        self.assertEqual(0, len(rev.shapes))
