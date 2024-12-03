***Notice : before running this code be sure to have***
---
**Needs**  
* **mtsd_fully_annotated_annotation.zip** from [**Mapillary trafic sign dataset**](https://www.mapillary.com/dataset/trafficsign)
    * contains the **annotations** for each image *.json* under `/annotations` folder.
        * Image annotation names are the same as image names, except for their extensions, which differ: *.json* and *.jpg*. **E.g.:**, `picture.json → picture.jpg`.
    * contains the **splits** for each **set** under `/splits` : `train.txt`, `test.txt` & `val.txt` 
* **mtsd_fully_annotated_images.val.zip** from [**Mapillary trafic sign dataset**](https://www.mapillary.com/dataset/trafficsign)
    * contains the validation images in *.jpg* under the `/images`folder. 

Thoses data must be place under `/src/datasets` as described below.
```
src/ 
 └── datasets/ 
      ├── images/
      ├── splits/
      └── annotations/
```

***NotaBene:*** As the complete dataset is enormous we will use only the **validation set** `val.txt` splitted in train, validation & test set. 

# Data preprocessing
# Roadmap

1.  `convert_data.ipynb` :  Generate the classes dictionnary `label_dict.json` and the whole (whole dataset) yolo annotation `/src/datasets/annotations_yolo/*` 
2.  `split_data.ipynb` : Split the set in 3 sets - train, val(validation) & test sets `/src/datasets/dataset/{train,test,val}/{images,labels}`
3.  `yolo.ipynb` : ***[ToDo complete here] The YOLO model***


# Notebook explanations

## read_data.ipynb

This is a basic test to visualize an image and its annotations.  
***needs to run this code :*** nothing


## convert_data.ipynb

This notebook allows to convert the annotations from a JSON file to a txt file in the format required by YOLO and generate a dictionary of classes.
dict_classes.json contains the classes of the objects in the dataset
The YOLO format is as follows:
```
<object-class> <x> <y> <width> <height>
```
where:
- `<object-class>` is the index of the object's class
- `<x> <y> <width> <height>` are the coordinates of the center of the bounding box and its width and height.
- The coordinates are normalized with respect to the image size.

***needs to run this code :*** 
* `annotations` from the **mtsd_fully_annotated_annotation.zip**  
***output :***
* `label_dict.json` : labels as categorical value
* `../datasets/annotations_yolo/<*filename>.txt`: annotations in *YOLO* format stored as *.txt* file  

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
***needs to run this code :***
* `label_dict.json` : 
* images : `/datasets/images/` from the **mtsd_fully_annotated_images.val.zip**
* `val.txt` : List of filenames that are used to create ou datasets from the `mtsd_v2_fully_annotated\splits`
* yolo's annotation labels : generated with the `convert_data.ipynb` script and stored in  `/datasets/annotations_yolo/*`

***output :***
* `dataset.yaml` : file containing the information about the data needed for *YOLO*.
* `dataset/<train,val, test>/images` : image files in *.jpg*
* `dataset/<train,val, test>/labels` : Yolo annotations for each image files in *.json*


## yolo.ipynb

This notebook allows you to launch YOLO training using the ultralytics library.



