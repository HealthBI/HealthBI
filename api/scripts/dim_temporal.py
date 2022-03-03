#!/usr/bin/python
import json
from pandas import *

class Temporal:
    """
    Temporal Object
    """
    def __init__(self, value, temporal_uid = None):
        self.uid = temporal_uid
        self.value = value

class DimTemporal(Temporal):
    """
    Shapes csv dim_temporal columns.
    """
    def __init__(self, json_file):
        self.json_file = json_file
        self.json_temporal_cols = []
        self.temporal_val = []
        self.temporal_objs = []

    def get_json_cols(self):
        """
        Get all json cols for temporal. Based off known required data model fields.
        Temporal columns: "Temporal_UID": {"column_name": "Year", "value": ""},
        returns if temporal is a column or value
        """
        with open(self.json_file) as json_file:
            dictData = json.load(json_file)
            for x in dictData['Temporal_UID']:
                if x == "value" and dictData['Temporal_UID'][x] != "":
                    value = dictData['Temporal_UID'][x]
                    return value, True
                else:
                    tmp_val = dictData['Temporal_UID'][x]
                    if tmp_val != '':
                        self.json_temporal_cols.append(tmp_val)
        return self.json_temporal_cols, False

    def get_csv_val(self, row, json_col):
        """
        This is only called if column_name was given in json.
        Gets the year value in row.
        """
        for key in row:
            if key in json_col:
                return row[key]
        return

    def create_new_temporal_object(self, value):
        """
        Create a new temporal object if unique value. Not given a temporal_uid.
        """
        if value not in self.temporal_val:
            self.temporal_val.append(value)
            self.temporal_objs.append(Temporal(value))