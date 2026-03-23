from flask import Flask, request, render_template
import pandas as pd
from data_reader import DataReader
from utils.data_converter import convert_to_dataframe
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
            df = convert_to_dataframe(data)

            if isinstance(df, pd.DataFrame):
                total_rows = len(df)
                preview_df = df.head(100)
                return f"<h3>Showing first 100 rows out of {total_rows}</h3>" + preview_df.to_html(index=False)
            else:
                return str(data)  # For non-DataFrame data, still show as-is (consider limiting if needed)

        # Case 2: API URL
        elif "api_url" in request.form:
            api_url = request.form["api_url"]
            reader = DataReader(api_url, source_type="api")
            data = reader.read()
            df = convert_to_dataframe(data)
            df.columns = df.columns.str.lower().str.strip()
            df = df.fillna("")
            return f"<h3>Showing first 100 rows out of {len(df)}</h3>" + df.head(100).to_html(index=False)

    return render_template("upload.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    read_app.run(host="0.0.0.0", port=port)
