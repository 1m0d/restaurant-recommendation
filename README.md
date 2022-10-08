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

### Example usage
#### Restaurant Recommendation
```bash
# Run restaurant recommendation with default settings
python main.py

# Run restaurant recommendation with decision tree model, saving the trained model
python main.py --classifier decisiontree --save_model_path ./datafiles/decisiontree.pickle

# Run restaurant recommendation with decision tree model, loading pretrained model
python main.py --classifier decisiontree --pretrained_model_path ./datafiles/decisiontree.pickle

# Run restaurant recommendation with variable system delay, capslock mode, and levenshtein distance set to 5
python main.py --delay --capslock --levenshtein 5
```

```
usage: main.py [-h] [--dataset_path DATASET_PATH] [--debug [DEBUG]] [--capslock [CAPSLOCK]] [--delay [DELAY]] [--levenshtein LEVENSHTEIN] [--classifier [{logregression,decisiontree,rulebased}]]
               [--pretrained_model_path PRETRAINED_MODEL_PATH] [--save_model_path SAVE_MODEL_PATH]
               [{evaluate,recommend}]

Restaurant Recommendation System

positional arguments:
  {evaluate,recommend}  main objective of program run, defaults to recommend restaurant (default: recommend)

optional arguments:
  -h, --help            show this help message and exit
  --dataset_path DATASET_PATH
                        path to dialog classification dataset (default: ./datafiles/dialog_acts.dat)
  --debug [DEBUG]       set loglevel to Debug (default: None)
  --capslock [CAPSLOCK]
                        print all system utterances in uppercase (default: False)
  --delay [DELAY]       enable variable system delay (default: False)
  --levenshtein LEVENSHTEIN
                        set the levenshtein distance (default: 3)
  --classifier [{logregression,decisiontree,rulebased}]
                        set the dialog act classifier (default: logregression)
  --pretrained_model_path PRETRAINED_MODEL_PATH
                        path to pretrained model, to use for restaurant recommendation (default: None)
  --save_model_path SAVE_MODEL_PATH
                        path to save classification model after training (default: None)```
```

#### Classifier Evaluation
```bash
python main.py evaluate
```
Experiment logging will be available in `experiment_logs` directory.
