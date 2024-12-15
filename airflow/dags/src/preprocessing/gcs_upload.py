import os
from google.cloud import storage
import random

# Define the folder for storing downloaded files
BUCKET_NAME = "mse_mapillary"
DATASET_FOLDER = "tmp/"


def split_data(local_folder, train_ratio=0.8, val_ratio=0.1):
    """Split image and annotation files into train, val, and test sets."""
    images_folder = os.path.join(local_folder, "images")
    annotations_folder = os.path.join(local_folder, "annotations_yolo")

    # Get all image file names (assuming all have matching annotations)
    image_files = [f for f in os.listdir(
        images_folder) if os.path.isfile(os.path.join(images_folder, f))]

    # Shuffle the data
    random.shuffle(image_files)

    # Split the data
    total_files = len(image_files)
    train_count = int(total_files * train_ratio)
    val_count = int(total_files * val_ratio)

    train_files = image_files[:train_count]
    val_files = image_files[train_count:train_count + val_count]
    test_files = image_files[train_count + val_count:]

    # Create output directories
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(local_folder, split, "images"), exist_ok=True)
        os.makedirs(os.path.join(local_folder, split, "labels"), exist_ok=True)

    # Move files to respective directories
    for split, file_list in zip(["train", "val", "test"], [train_files, val_files, test_files]):
        for file_name in file_list:
            # Move image file
            image_src = os.path.join(images_folder, file_name)
            image_dest = os.path.join(local_folder, split, "images", file_name)
            os.rename(image_src, image_dest)

            # Move corresponding annotation file
            annotation_src = os.path.join(
                annotations_folder, file_name.replace('.jpg', '.txt'))
            annotation_dest = os.path.join(
                local_folder, split, "labels", file_name.replace('.jpg', '.txt'))
            if os.path.exists(annotation_src):
                os.rename(annotation_src, annotation_dest)
            else:
                print(f"Warning: Annotation file not found for {file_name}")


def upload_new_data(SERVICE_ACCOUNT_JSON):
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    bucket = client.get_bucket(BUCKET_NAME)

    for split in ["train", "val", "test"]:
        split_folder = os.path.join(DATASET_FOLDER, split)
        for root, _, files in os.walk(split_folder):
            for file_name in files:
                local_path = os.path.join(root, file_name)
                # Preserve folder structure
                gcs_path = os.path.join("dataset", os.path.relpath(local_path, DATASET_FOLDER))
                blob = bucket.blob(gcs_path)
                blob.upload_from_filename(local_path)
                print(f"Uploaded {
                    local_path} to gs://{gcs_path}")
