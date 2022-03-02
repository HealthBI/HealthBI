import os
import re
from random import randint
from signal import valid_signals
import sys
import csv
import json
from pandas import *
class Temporal:
    def __init__(self, temporal):
        self.temporal_uid = None
        self.temporal = temporal

# [2021, 2102, 2131]
# [2021, lcoation, indicator, value]

class DimTemporal():
    """
    Shapes csv dim_temporal columns.
    """
    def __init__(self, csv_file, json_file, db_conn, db_cur):
        self.csv_file = csv_file
        self.json_file = json_file
        self.db_conn = db_conn
        self.db_cur = db_cur
        self.json_temporal_cols = []
        self.temporal_vals = {}

    def get_json_cols(self):
        """
        Get all json cols for temporal. Based off known required data model fields.
        Temporal columns: "Temporal_UID": {"column_name": "Year", "value": ""},
        returns if temporal is a column or value
        """
        with open(self.json_file) as json_file:
            dictData = json.load(json_file)
            for x in dictData['Temporal_UID']:
                tmp = dictData['Temporal_UID'][x]
                self.json_temporal_cols.append(tmp)
        return self.json_temporal_cols

    def get_csv_vals(self, json_cols):
        """
        This is only called if column_name was given in json
        """
        key = json_cols[0]
        with open(self.csv_file, mode='r', encoding="utf-8-sig") as csv_file:
            data = read_csv(self.csv_file)
            self.temporal_vals[key] = data[key].tolist()
        # Remove duplicate values in list
        for i in self.temporal_vals:
            tmp = []
            [tmp.append(x) for x in self.temporal_vals[i] if x not in tmp]
            self.temporal_vals[i] = tmp

    def increment_temporal(self, column_name, value):

        self.db_cur.execute("SELECT LAST(temporal_uid) FROM dim_temporal")
        temporal = self.db_cur.fetchall()

        num = int(re.findall('[0-9]+', temporal))
        num += 1
        
        tem = "tem" + str(int)

        return tem
    
    def do_value_injection(self, value):
        """
        This is called when a value is given as the Temporal_UID.
        """
        sql = "INSERT INTO dim_temporal VALUES ('6', %s, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA')"
        self.db_cur.execute(sql, [value])
        self.db_conn.commit()
        print(self.db_cur.rowcount, "records inserted.")

        self.db_cur.execute("select * from dim_temporal")
        result = self.db_cur.fetchall()
        print(result)
    
    def do_data_injection(self):
        """
        if given a column_name:
            For every value in temporal column, inject into the dim_temporal table
        """
        #TODO: create unique temproral_uid
        sql = "INSERT INTO dim_temporal VALUES ('7', %s, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA')"
        col_name = self.json_temporal_cols[0]
        all_vals = self.temporal_vals.get(col_name)
        print(all_vals)
        # wrap all vals in a tuple
        self.db_cur.executemany(sql, [all_vals])
        self.db_conn.commit()
        print(self.db_cur.rowcount, "records inserted.")

        self.db_cur.execute("select * from dim_temporal")
        result = self.db_cur.fetchall()
        print(result)

    # TODO: create new object for every new temporal object (1. 2021, 2. 2022)