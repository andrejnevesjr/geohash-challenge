import os
from re import L
import sys
import pandas as pd
from bisect import bisect_left
from dataclasses import dataclass
from typing import Dict, List
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))


@dataclass
class PrefixHandler:
    """Class for handle prefix search."""

    def geohash_dict_to_df(self, geohash_short_prefix: Dict) -> pd.DataFrame:
        """ Function to convert the dictionary with geohash enriched data.

        Args:
            geohash_short_prefix (Dict): Dict with data to be converted

        Returns:
            pd.DataFrame: Dataframe with geohash and shortest prefix
        """
        geohash_lookup = [{"geohash": key, "unique_prefix": value} for key, value in geohash_short_prefix.items()]
        geohash_enriched_df = pd.DataFrame(geohash_lookup)
        return geohash_enriched_df

    def prefix_exists(self, geohash_list: List, geohash_prefix: str) -> bool:
        """_summary_

        Args:
            geohash_list (List): List with all geohashes
            geohash_prefix (str): Prefix that must be checked

        Returns:
            bool: Return if prefix exists or not
        """
        try:
            return geohash_list[bisect_left(geohash_list, geohash_prefix)].startswith(geohash_prefix)
        except IndexError:
            return False

    def get_geohash_prefixes(self, geohash_code: str) -> List:
        """Generate all possible geohash prefixes

        Args:
            geohash_code (str): GeoHash code

        Returns:
            List: List with all possible geohash prefixes
        """
        geohash_prefixes_list = []
        for letter in range(1, len(geohash_code)+1):
            prefix = geohash_code[:letter]
            geohash_prefixes_list.append(prefix)
        return geohash_prefixes_list

    def get_shortest_prefix(self, geohash_prefixes_map: List,
                            geohash_list: List,
                            geohash_code: str) -> Dict:
        """Find the shortest prefix to a respective Geohash

        Args:
            geohash_prefixes_map (List): Map with all possible geohash prefixes
            geohash_list (List): List will all geohashes
            geohash_code (str): Current Geohash code being searched

        Returns:
            Dict: Returns a Map with Geohash and shortest prefix
        """
        geohash_aux_list = geohash_list.copy()
        geohash_aux_list.pop(geohash_aux_list.index(geohash_code))
        geohash_output_map = {}

        for geohash_prefix in geohash_prefixes_map:
            is_present = self.prefix_exists(geohash_aux_list, geohash_prefix)
            # If shortest prefix was not added it will include now
            if not is_present and (geohash_code not in geohash_output_map.keys()):
                geohash_output_map[geohash_code] = geohash_prefix
                return geohash_output_map

    def geohash_mapper(self, geohash_list: List) -> pd.DataFrame:
        """ Call functions responsible for enrich GeoHash with shortest prefix

        Args:
            geohash_list (List): List with all geohashes

        Returns:
            pd.DataFrame: DataFrame containing enriched data
        """
        prefix_shortest_list = {}

        for geohash_code in geohash_list:
            geohash_prefixes_map = self.get_geohash_prefixes(geohash_code)
            geohash_shortest_map = self.get_shortest_prefix(geohash_prefixes_map,
                                                            geohash_list,
                                                            geohash_code)

            prefix_shortest_list[geohash_code] = geohash_shortest_map[geohash_code]
        return self.geohash_dict_to_df(prefix_shortest_list)
