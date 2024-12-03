# AirFlow - panneau 
## List of tasks
* [x] Local preprocessing of the data
* [ ] Check if airflow can manage and versionize data (if not use dvc as data manager & data version controller)
* [ ] Store data either in the cloud or locally - locally for developpment purpose
* [ ] Create DAG - Directed Acyclic Graph - with a few steps
    * [ ] Task - preprocessing
    * [ ] Task - Upload preprocessed files - if in cloud
    * [ ] Task - Retrain the model
    * [ ] Task - Predict using the model
    * [ ] Task - Give metrics
