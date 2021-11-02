
import pandas as pd


def dataframe_of_json(json_file: str) -> pd.DataFrame:
    return pd.io.json.read_json(json_file, orient='records')
