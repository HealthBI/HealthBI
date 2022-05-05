import json
from pandas import *

class Dataset:

    def __init__(self, dataset_uid, dataset_name, datasource_uid):
        self.dataset_uid = dataset_uid
        self.dataset_name = dataset_name
        self.datasource_uid = datasource_uid

class ImpDataset:

    def __init__(self, json_file):
        self.json_file = json_file
        self.json_dataset_cols = {}
        self.dataset_vals = []
        self.datasets = []

    def get_json_cols(self):
        with open(self.json_file) as json_file:
            dictData = json.load(json_file)
            for x in dictData["DataSet_UID"]:
                if x == "value" and dictData["DataSet_UID"][x] != "":
                    value = dictData["DataSet_UID"][x]
                    return value, True
                else:
                    tmp_val = dictData["DataSet_UID"][x]
                    if tmp_val != "":
                        self.json_dataset_cols.append(tmp_val)

        return False

    def get_csv_val(self, row, json_col):
        pairs = {}
        
        for key in row:
            for i in self.json_dataset_cols:
                if self.json_dataset_cols[i] in row and self.json_dataset_cols[i] == key:
                    if self.json_dataset_cols[i] not in pairs:
                        pairs[i] = row[key]
                else:
                    pairs[i] = ""
        
        self.dataset_vals.append(pairs)
        return pairs

    def create_new_dataset_object(self):
        pass