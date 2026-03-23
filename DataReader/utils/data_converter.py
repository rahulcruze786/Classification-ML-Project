import pandas as pd

def convert_to_dataframe(data):

    # Case 1: Already DataFrame
    if isinstance(data, pd.DataFrame):
        return data

    # Case 2: List of dicts
    elif isinstance(data, list):
        return pd.DataFrame(data)

    # Case 3: Dictionary
    elif isinstance(data, dict):
        return pd.DataFrame([data])

    # Case 4: String (JSON or raw)
    elif isinstance(data, str):
        try:
            return pd.read_json(data)
        except:
            return pd.DataFrame({"raw_data": [data]})

    # Case 5: Fallback
    else:
        return pd.DataFrame({"raw_data": [str(data)]})