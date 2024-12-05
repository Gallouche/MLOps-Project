# Report: Pipeline AirFlow

Ernst Tim, Gallandat Théo, Guidetti Laetitia, Küenzi Jean-Daniel, Perez Yohann

## Introduction

This project aims to set up an AirFlow pipeline to perform all the steps of a Machine Learning project. The pipeline should allow to download the data, preprocess it, train a model and evaluate it. This approach allows to automate the process, make it reproducible and understand the advantages and disadvantages of using an AirFlow pipeline.

### AirFlow

Apache Airflow is a workflow management platform that allows to schedule, monitor, automate, and manage workflows. It is open source, Python native, and was developed by Airbnb in 2015. His principles are scalable, dynamic pipeline generation, easily extensible and explicit.

Workflows are represented as Directed Acyclic Graphs (DAGs). A DAG is composed of tasks that are individual units of work. Tasks can be of different types, such as Python functions, SQL queries, or Bash scripts. Tasks can be chained together and dependencies can be defined between them. It is possible to make decisions based on the result of a task. There is a wide range of providers for AirFlow, which allow to connect to different services such as AWS, Google Cloud, Azure, etc.

### Use case

The use case chosen for this project is the training of a YOLOv8 model to detect road signs in images. The goal is to train a model that can detect the road signs in the images and draw bounding boxes around them.

This is a common problem in the field of road safety and autonomous driving. It is an important task for the development of navigation and automatic driving systems. It allows to identify road signs on the road and to take the necessary measures according to the information they provide.

For this, the objective is to realize the following configuration:

![Diagram](images/project-diagram.png)

This requires breaking down the process into several tasks that will be executed by the AirFlow pipeline. All tasks allow the completion of a complete Machine Learning project, from data retrieval to model evaluation through training. The pipeline will be composed of the following tasks:
- TODO

## Dataset

The dataset comes from Mapillary, a platform containing street images and map data from around the world. Mapillary Traffic Sign Dataset is a dataset of annotated road sign images in the form of bounding boxes. It contains 100,000 images annotated with 400 classes of road signs on 6 continents with a wide variety of weather conditions and brightness.

For each image, there is a JSON file containing the annotations of the road signs.

Image example:

![Image example](images/example_mapillary.png)


## Pipeline description

### Task - preprocessing

### Task - Upload preprocessed files - if in cloud

### Task - Retrain the model

### Task - Predict using the model

### Task - Give metrics

## Advantage of using AirFlow pipeline

This use case is an example of using a pipeline to automate the process of training a model. It allows to see the different advantages of using this type of tool.

The advantages of using a pipeline are as follows:

- Automation of the process: all steps are automated and traceable. It is not necessary to manually run scripts or execute commands for each step. There is therefore no risk of human error.
- Repeatability: the pipeline can be restarted at any time to reproduce the results. This allows to test different configurations and compare the results.
- Monitoring: the pipeline allows to monitor the progress of the process. It is possible to see when a task was executed and if it failed. If a problem occurs, it is easy to identify and therefore to correct. This is not possible when the steps are executed manually.
- Collaboration: the pipeline allows to easily share the process with other people. It is possible to see the results of the different steps and compare them. There is no risk of confusion about the steps to follow or compatibility issues between the versions of the software used.
- Modularity: the pipeline is composed of different tasks that can be reused for other projects. It is also possible to modify a task without affecting the others in order to test different configurations.
- Scalability: the pipeline can be scaled to handle large datasets and complex workflows. It can be run on a single machine or distributed across multiple machines to speed up the process.

The main disadvantage of using an AirFlow pipeline is the time required to set it up. It is necessary to understand how AirFlow works, how to create a pipeline and how to configure the different tasks. This can take time and requires technical skills.

## Difficulties encountered

FF

## Conclusion