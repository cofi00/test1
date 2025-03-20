from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

# Povezivanje sa Google Cloud Storage
BUCKET_NAME = "my-files-marketplace"

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
    
    file_url = upload_to_gcs(file, destination_blob_name)
    
    return jsonify({"message": "File uploaded", "file_url": file_url})

@app.route('/')
def home():
    return "Cloud Run backend is running!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
