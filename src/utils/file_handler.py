import os
import gzip
import sys
import pandas as pd
from typing import List
from dataclasses import dataclass
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
from custom_exception import MoveFileException, DecompressException, ReadCSVException


@dataclass
class CustomFileHandler:
    """Class for read, decompress and move all input files."""
    _source_path: str
    _target_path: str = None

    @property
    def source_path(self) -> str:
        return self._source_path

    @property
    def target_path(self) -> str:
        return self._target_path

    def list_path_files(self, path_to_check: str) -> List:
        """List all files that were received on Landing layer

        Returns:
            List: List of files available
        """
        list_of_objects = os.listdir(path_to_check)
        return list_of_objects

    def decompress_file(self, infile: str) -> str:
        """Decompress GZ files

        Args:
            infile (str): path to files to be decompressed

        Returns:
            str: file contents
        """
        decom_str = ""
        try:
            with open(infile, 'rb') as inf:
                decom_str = gzip.decompress(inf.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"File not found :: {infile}")
            sys.exit(1)
        except Exception:
            raise DecompressException(infile)

        return decom_str

    def move_landing_to_raw(self, files_to_extract: List,
                            path_raw: str) -> bool:
        """ Receive list of files, decompress and move to RAW layer

        Args:
            files_to_extract (List): Files to be decompressed and moved.
            path_raw (str): Path to RAW layer

        Raises:
            Exception: Failed on decompress or save file

        Returns:
            bool: Pipeline status
        """
        is_done = False
        try:
            for path_file in files_to_extract:
                #  Extract filename
                filename = os.path.splitext(os.path.basename(path_file))[0]
                #  Decompress file
                data = self.decompress_file(path_file)
                # Path to send it to RAW layer
                full_path = path_raw + "/" + filename
                # Write file decompressed
                with open(full_path, 'w', encoding='utf8') as tof:
                    tof.write(data)
                # Update pipeline status
                is_done = True
        except (FileNotFoundError, MoveFileException):
            print(f"Something whent wrong while moving file :: {full_path}")

        return is_done

    def read_csv(self, infile: str) -> pd.DataFrame:
        """Read CSV files

        Args:
            infile (str): path to files to be read

        Returns:
           pd.DataFrame: List with latitude and longitude data.
        """
        # list_positions = []
        df = pd.DataFrame()
        df_column_names = ["latitude", "longitude"]
        try:
            df = pd.read_csv(infile, names=df_column_names, skiprows=1)
        except (FileNotFoundError, ReadCSVException):
            print(f"Error while reading file :: {infile}")

        return df
