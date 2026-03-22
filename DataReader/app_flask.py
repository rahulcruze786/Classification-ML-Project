from flask import Flask, request, render_template
import pandas as pd
from data_reader import DataReader
import os

read_app = Flask(__name__)
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@read_app.route("/", methods=["GET", "POST"])


def upload_file():
    if request.method == "POST":
        # Case 1: File upload
        if "file" in request.files:
            file = request.files["file"]
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            ext = file.filename.split(".")[-1].lower()
            reader = DataReader(file_path, source_type="local", file_format=ext)
            data = reader.read()

            if isinstance(data, pd.DataFrame):
                return data.to_html()
            else:
                return str(data)

        # Case 2: API URL
        elif "api_url" in request.form:
            api_url = request.form["api_url"]
            reader = DataReader(api_url, source_type="api")
            data = reader.read()
            return str(data)

    return render_template("upload.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    read_app.run(host="0.0.0.0", port=port)
