# DVC instructions

Here are instructions to prepare the DVC pipeline and track data.

## Install DVC
```
pip install dvc
```

## Initialization of DVC
``shell
dvc init
``

## Run the preparation of data
```shell
python3.12 <prepare_script.py> <raw_folder> <processed_folder>
```

## Train the model with the prepared data and save it 
```shell
python3.12 <train_script.py> <processed_data_folder> <model_folder>
```

## Evaluate model (not mandatory)
```shell
python3.12 <evaluate_script.py> <model_folder> <processed_data>
```

# Add stages to DVC

## Prepare stage
```shell
dvc stage add -n prepare \
    -p prepare \
    -d src/prepare.py -d src/utils/seed.py -d data/raw \
    -o data/prepared \
    python3.12 src/prepare.py data/raw data/prepared
```

## Train stage
```shell

dvc stage add -n train \
    -p train \
    -d src/train.py -d src/utils/seed.py -d data/prepared \
    -o model \
    python3.12 src/train.py data/prepared model
```

## Evaluate stage
```shell
dvc stage add -n evaluate \
    -d src/evaluate.py -d model \
    --metrics evaluation/metrics.json \
    --plots evaluation/plots/confusion_matrix.png \
    --plots evaluation/plots/pred_preview.png \
    --plots evaluation/plots/training_history.png \
    python3.11 src/evaluate.py model data/prepared
```


# Show dag
```shell
dvc dag
```

# Execute the whole pipeline
```shell
dvc repro
```


-- ## DVC add raw data

-- ```shell
-- dvc add data/raw/
-- dvc config core.autostage true
-- ```
