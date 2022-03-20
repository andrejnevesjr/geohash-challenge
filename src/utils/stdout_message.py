import os
import sys
import pandas as pd
from dataclasses import dataclass
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))


@dataclass
class StdoutMessage():
    """Class Print Messages to stdout."""

    @staticmethod
    def generic_output(message_code: int) -> None:
        """Print Generic messages to the process."""
        messages = {1: "#"*27 + "\n    Starting Challenge\n" + "#"*27 + "\n",
                    2: "#"*27 + "\n    Preparing Pipeline\n" + "#"*27 + "\n",
                    3: "#"*27 + "\n    Running Pipeline\n" + "#"*27 + "\n",
                    4: "#"*27 + "\n    Pipeline Completed\n" + "#"*27 + "\n",
                    5: "#"*27 + "\n    Printing Results\n" + "#"*27 + "\n",
                    'default': "#"*27 + "\nDummy Message\n" + "#"*27 + "\n"
                    }

        sys.stdout.write(messages.get(message_code, 'default'))

    @staticmethod
    def challenge_ouput(df_to_print: pd.DataFrame) -> bool:
        """ Print DataFrame to Stdout

        Returns:
            bool: Return True if everything was printed out.
        """
        is_completed = False
        output_stdout = []
        try:
            output_stdout = ["lat,lng,geohash,uniq"]
            geohash_df_to_list = df_to_print.values.tolist()
            geohash_df_to_list = [",".join(map(str, rows)) for rows in geohash_df_to_list]
            output_stdout.extend(geohash_df_to_list)
            StdoutMessage.generic_output(5)
            print(*output_stdout, sep="\n")
            is_completed = True
        except Exception:
            pass
        return is_completed
