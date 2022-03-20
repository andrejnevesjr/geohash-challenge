import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "challenge", "utils"))
from prefix_handler import PrefixHandler


class TestPrefixHandler(unittest.TestCase):
    def test_get_geohash_prefixes(self):
        list_with_all_prefixes = ['s', 'sp', 'sp3', 'sp3e', 'sp3e3', 'sp3e3q',
                                  'sp3e3qe', 'sp3e3qe7', 'sp3e3qe7m',
                                  'sp3e3qe7mk', 'sp3e3qe7mkc', 'sp3e3qe7mkcb']
        prefix_handler = PrefixHandler()
        geohash_code = "sp3e3qe7mkcb"
        prefixes = prefix_handler.get_geohash_prefixes(geohash_code)
        self.assertEqual(list_with_all_prefixes, prefixes)

    def test_get_shortest_prefix(self):
        geohash_prefixes_map = ['s', 'sp', 'sp3', 'sp3e', 'sp3e3', 'sp3e3q',
                                'sp3e3qe', 'sp3e3qe7', 'sp3e3qe7m',
                                'sp3e3qe7mk', 'sp3e3qe7mkc', 'sp3e3qe7mkcb']
        geohash_code = "sp3e3qe7mkcb"
        geohash_list = ['ezjmgcj3udcp', 'ezjmgcj3f1k0', 'ezjmgcjrv4hs',
                        'ezjmgw7sxrgp', 'ezjqh1kyq9pd', 'sp3e3qe7mkcb',
                        'sp3e2wuys9dr', 'sp3e2wuzpnhr']

        prefix_handler = PrefixHandler()
        shortest = prefix_handler.get_shortest_prefix(geohash_prefixes_map,
                                                      geohash_list,
                                                      geohash_code)
        self.assertEqual("sp3e3", shortest[geohash_code])
