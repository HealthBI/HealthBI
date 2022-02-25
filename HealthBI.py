#!/usr/bin/python
import os
import sys
from api.scripts.dim_temporal import dim_temporal

class HealthBI:
    """
    HealthBI.py takes in a csv file as an argument and shapes it to fit the data model.
    """
    def __init__(self, csv_file):
        self.csv_file = csv_file

    
    def shape_csv(self):
        #ready by row
        self.shape_dim_temporal()
        self.shape_dim_location()
        self.shape_var_indicator()
        self.creatFact()

    def run_injections(self):
        pass

    def shape_dim_temporal(self):
        dim_temporal(self.csv_file)

if __name__=="__main__":
    if len(sys.argv) == 3:
        file_exists = os.path.exists(sys.argv[1])
        file_exists = os.path.exists(sys.argv[2])
        if file_exists == True:
            csvdata = HealthBI(sys.argv[1])
        else:
            print("File does not exist.")
    else:
        print("Usage: python HealthBI.py file")
