# Notebook explaining

## read_data.ipynb

This is a basic test to visualize an image and its annotations.

## convert_data.ipynb

This notebook allows to convert the annotations from a JSON file to a txt file in the format required by YOLO and generate a dictionary of classes.
The YOLO format is as follows:
```
<object-class> <x> <y> <width> <height>
```
where:
- `<object-class>` is the index of the object's class
- `<x> <y> <width> <height>` are the coordinates of the center of the bounding box and its width and height.
- The coordinates are normalized with respect to the image size.

## split_data.ipynb

Split the data into the following tree:

```
dataset/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

Generate a dataset.yaml file containing the information about the data needed for YOLO.

## yolo.ipynb

Ce notebook permet de lancer des entrainements de YOLO en utilisant la librairie ultralytics.



