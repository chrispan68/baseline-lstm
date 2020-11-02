import json
import sys
import os
import random

random.seed(100)
directory = sys.argv[1]

data_splits = {
    "train": 50000,
    "valid": 5000,
    "test": 5000
}

for data_set in data_splits:
    inp = data_set + '.json'
    out = data_set + '.txt'
    data = []
    with open(os.path.join(directory, inp)) as f:
        data = json.load(f)
    
    with open(os.path.join(directory, out), 'w') as f_out:
        for ex in random.sample(data, data_splits[data_set]):
            gender = ""
            if ex['gender'] == 'male':
                gender = '<MALE>: '
            else:
                gender = '<FEMALE>: '
            f_out.write(gender + ex['text'] + "\n")
        f_out.close()
