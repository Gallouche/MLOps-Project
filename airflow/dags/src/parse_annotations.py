import json
import os

WORK_DIR = "./tmp"


def count_element_per_label(json_dir):
    label_dict = {}

    # Iterate over all JSON files in the directory
    for json_file in os.listdir(json_dir):
        if json_file.endswith(".json"):
            with open(os.path.join(json_dir, json_file), 'r') as f:
                data = json.load(f)
                for obj in data.get('objects', []):
                    label = obj['label']
                    # Count the occurrences of each label
                    if label not in label_dict:
                        label_dict[label] = 1
                    else:
                        label_dict[label] += 1
    return label_dict


def generate_label_dict(json_dir, min_occurrences=500):
    # Count the occurrences of each label
    label_dict = count_element_per_label(json_dir)

    # Filter the labels with less than min_occurrences occurrences
    label_dict = {k: v for k, v in label_dict.items() if v >= min_occurrences}

    # Generate the label dictionary
    label_dict = {label: i for i, label in enumerate(label_dict.keys())}

    return label_dict


def convert_to_yolo(json_path, output_dir, label_dict):
    # Load the json file
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Read the image width and height from the JSON
    image_width = data['width']
    image_height = data['height']

    # Initialize the list to store annotations
    annotations = []

    # Iterate over all objects in the JSON
    for obj in data['objects']:
        label = obj['label']
        if label not in label_dict:
            continue  # Ignore the label if not in the dictionary

        class_id = label_dict[label]
        bbox = obj['bbox']

        # Extract the coordinates
        xmin, ymin, xmax, ymax = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']

        # Normalize the coordinates
        x_center = ((xmin + xmax) / 2) / image_width
        y_center = ((ymin + ymax) / 2) / image_height
        width = (xmax - xmin) / image_width
        height = (ymax - ymin) / image_height

        # Append the annotation in YOLO format
        annotations.append(f"{class_id} {x_center:.6f} {
                           y_center:.6f} {width:.6f} {height:.6f}")

    # Save the annotations to a text file
    output_file = os.path.join(output_dir, os.path.splitext(
        os.path.basename(json_path))[0] + ".txt")
    with open(output_file, 'w') as f:
        f.write("\n".join(annotations))


def convert_all_to_yolo(json_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    label_dict = generate_label_dict(json_directory, min_occurrences=500)
    print("Dictionnaire généré :", label_dict)
    for json_file in os.listdir(json_directory):
        if json_file.endswith(".json"):
            json_path = os.path.join(json_directory, json_file)
            convert_to_yolo(json_path, output_directory, label_dict)

    print(f"Annotations sauvegardées dans : {output_directory}")
