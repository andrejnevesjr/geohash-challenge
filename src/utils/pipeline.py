import os
import sys
from datetime import datetime
from dataclasses import dataclass
import gc
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
from file_handler import CustomFileHandler
from geohash_handler import GeoHashHandler
from prefix_handler import PrefixHandler
from stdout_message import StdoutMessage


@dataclass
class Pipeline:
    """Class for build and run pipeline end to end."""

    def prepare_pipeline(self, input_path: str, output_path: str) -> bool:
        """Prepare the pipeline to be executed moving required files.

        Args:
            input_path (str): Input path where files must be retrieved
            output_path (str): Target path where files must be moved to

        Returns:
            bool: Indicate if the pipeline should be executed
        """
        is_read_to_run = False
        # Get CustomFileHandler instance
        file_reader = CustomFileHandler(input_path, output_path)
        # Get files on Landing
        files_on_landing = file_reader.list_path_files(input_path)

        if len(files_on_landing) > 0:

            list_of_files = []
            # Create mount point to files on Landing
            for each_file in files_on_landing:
                full_path = file_reader.source_path + "/" + each_file
                list_of_files.append(full_path)

            # Move files from Landing to RAW (decompressed)
            is_read_to_run = file_reader.move_landing_to_raw(list_of_files,
                                                             output_path)

        return is_read_to_run

    def run_pipeline(self, raw_path: str) -> bool:
        """ Run pipeline to geohash enrichment

        Args:
            raw_path (str): Path to RAW layer.

        Returns:
            bool: True if pipeline was run successfully
        """
        is_completed = False
        # Get CustomFileHandler instance
        file_reader = CustomFileHandler(raw_path)
        # Get GeoHashHandler instance
        geohash_handler = GeoHashHandler()
        # Get PrefixHandler instance
        prefix_handler = PrefixHandler()
        # Get files on RAW
        files_on_raw = file_reader.list_path_files(raw_path)
        # Word used quite often for actions
        geo_keyword = "geohash"
        if len(files_on_raw) > 0:
            # Create mount point to files on RAW
            for each_file in files_on_raw:
                full_path = file_reader.source_path + "/" + each_file
                df_geo_coodinates = file_reader.read_csv(full_path)
                df_geo_coodinates[geo_keyword] = df_geo_coodinates.apply(
                        lambda x: geohash_handler.geohash_from_position(x.latitude, x.longitude),
                        axis=1
                    )
                geohash_prefix_unique_list = list(set(df_geo_coodinates[geo_keyword].values))
                # Search prefix among all entries
                geohash_sorted_list = sorted(geohash_prefix_unique_list)
                geohash_short_unique_prefix = prefix_handler.geohash_mapper(geohash_sorted_list)

                # Merge DataFrames
                df_geohash_result = df_geo_coodinates.merge(geohash_short_unique_prefix,
                                                            on=geo_keyword,
                                                            how='left')
                # Clean coodinates
                del df_geo_coodinates
                gc.collect()
                # Print to Stdout
                is_completed = StdoutMessage.challenge_ouput(df_geohash_result)
        return is_completed
