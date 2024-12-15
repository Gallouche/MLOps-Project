import os
from google.cloud import storage

# Define the folder for storing downloaded files
BUCKET_NAME = "dataset_drop"
DATASET_FOLDER = "tmp/"


def download_and_delete_files_from_gcs(SERVICE_ACCOUNT_JSON):
    """Download all files from a Google Storage bucket and delete them, preserving folder structure."""
    # Initialize Google Cloud Storage client
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    bucket = client.get_bucket(BUCKET_NAME)

    blobs = bucket.list_blobs()
    for blob in blobs:
        # Preserve folder structure
        local_path = os.path.join(DATASET_FOLDER, blob.name)

        # If the blob is a directory, skip it
        if blob.name.endswith("/"):
            print(f"Skipping directory: {blob.name}")
            continue

        local_dir = os.path.dirname(local_path)

        # Ensure the local directory exists
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        # Download the file
        blob.download_to_filename(local_path)
        print(f"Downloaded: {blob.name} to {local_path}")

        # Delete the file from the bucket
        blob.delete()
        print(f"Deleted: {blob.name} from bucket {BUCKET_NAME}")
