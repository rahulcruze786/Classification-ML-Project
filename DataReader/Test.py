from data_reader import DataReader

# Test local CSV
reader = DataReader("sample.csv", source_type="local", file_format="csv")
print(reader.read())

# Test API
reader = DataReader("https://api.example.com/data", source_type="api")
print(reader.read())