import os
import sys
from typing import Tuple
from dataclasses import dataclass
import geohash
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))


@dataclass
class GeoHashHandler:
    """Class for handle GeoHash actions."""

    def geohash_from_position(self, latitude: float, longitude: float) -> str:
        """Convert coordinates to a GeoHash

        Args:
            latitude (float): the measurement of distance north or south
            longitude (float): the measurement of distance east or west
        Returns:
            str: cordinates converted to a respective geohash
        """
        code_geohash = geohash.encode(latitude, longitude)
        return code_geohash

    def position_from_geohash(self, code_geohash: str) -> Tuple:
        """Convert GeoHash to coordinates

        Args:
            code_geohash (str): the geohash code
        Returns:
            List: cordinates converted from geohash
        """
        coordinates = geohash.decode(code_geohash)
        return coordinates
