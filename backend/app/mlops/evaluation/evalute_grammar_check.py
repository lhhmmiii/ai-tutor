import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
import pandas as pd

def preprocess_data(data_path: str = "app/mlops/evaluation/GrammarTestset.csv"):
    data = pd.read_csv(data_path)
    data = data[['Error Type', 'Ungrammatical Statement', 'Standard English']]
    data = data.rename(columns={
        'Ungrammatical Statement': 'text',
        'Standard English': 'label'
    })
    return data

data = preprocess_data()
print(data.head())