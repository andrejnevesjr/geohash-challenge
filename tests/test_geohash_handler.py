import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "challenge", "utils"))
from geohash_handler import GeoHashHandler


class TestGeoHashHandler(unittest.TestCase):
    def test_geohash_from_position(self):
        geohash_handler = GeoHashHandler()
        latitude = 41.388828145321
        longitude = 2.1689976634898
        geohash_code = geohash_handler.geohash_from_position(latitude,
                                                            longitude)
        self.assertEqual("sp3e3qe7mkcb", geohash_code)

    def test_position_from_geohash(self):
        geohash_handler = GeoHashHandler()
        geohash_code = "sp3e3qe7mkcb"
        coordinates = geohash_handler.position_from_geohash(geohash_code)
        self.assertEqual((41.38882809318602, 2.1689976565539837), coordinates)
