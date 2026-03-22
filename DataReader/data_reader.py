import os
import json
import pandas as pd
import requests


class DataReader:
    """
    Read data from:
    - Local user-uploaded files (CSV, Excel, JSON, TXT)
    - APIs (JSON responses)
    """

    def __init__(self, source: str, source_type: str, file_format=None):
        self.source = source
        self.source_type = source_type
        self.file_format = file_format

    def read(self):
        if self.source_type == "local":
            return self._read_local()
        elif self.source_type == "api":
            return self._read_api()
        else:
            raise ValueError("Unsupported source_type : ", self.source_type)
        
    def _read_local(self):
        if not os.path.exists(self.source):
            raise FileNotFoundError("File not found : " + self.source)
        
        if self.file_format == "csv":
            return pd.read_csv(self.source)
        elif self.file_format == "xlsx":
            return pd.read_excel(self.source)
        elif self.file_format == "txt":
            with open(self.source, "r") as f:
                return f.read()
        elif self.file_format == "json":
            with open(self.source,"r") as f:
                return json.load(f)
        else:
            raise ValueError ("Unsupported file format : " + str(self.file_format))

    def _read_api(self):
        response = requests.get(self.source)
        response.raise_for_status()
        return response.json()