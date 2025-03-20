from flask import Flask, request, jsonify
from google.cloud import storage
from flask_cors import CORS  # Uvozimo CORS

app = Flask(__name__)

# Omogućavanje CORS za sve domene (možeš biti specifičniji ako želiš)
CORS(app, resources={r"/*": {"origins": "*"}})  # Dozvoljava sve domene

# Povezivanje sa Google Cloud Storage
BUCKET_NAME = "filipbajevic1"

def upload_to_gcs(file, destination_blob_name):
    """Upload fajla na Google Cloud Storage"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file)
    blob.make_public()
    return blob.public_url

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    destination_blob_name = f"uploads/{file.filename}"
    
    try:
        file_url = upload_to_gcs(file, destination_blob_name)
        return jsonify({"message": "File uploaded", "file_url": file_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "Cloud Run backend is running!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


