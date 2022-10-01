# Restaurant Recommendation Dialog System

## Environment Setup
```shell
pip install pipenv
pipenv install
```

## Run
enter virtual environment
```shell
pipenv shell
```

```shell
python main.py
```
```
usage: main.py [-h] [--dataset_path DATASET_PATH] [--debug [DEBUG]] [{evaluate,recommend}]

text classification

positional arguments:
  {evaluate,recommend}  main objective of program run, defaults to recommend restaurant

optional arguments:
  -h, --help            show this help message and exit
  --dataset_path DATASET_PATH
                        path to dialog classification dataset
  --debug [DEBUG]       set loglevel to Debug
```

Experiment logging will be available in `experiment_logs` directory.
