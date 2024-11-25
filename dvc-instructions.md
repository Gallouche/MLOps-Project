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

## DVC add raw data

```shell
dvc add data/raw/
dvc config core.autostage true
```
