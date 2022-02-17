#!/usr/bin/python
import os
import sys
from api.shapeCSV import shapeCSV

"""
HealthBI.py takes in a csv file as an argument and shapes it to fit the data model.
"""

if __name__=="__main__":
    if len(sys.argv) == 2:
        file_exists = os.path.exists(sys.argv[1])
        if file_exists == True:
            csvdata = shapeCSV(sys.argv[1])
        else:
            print("File does not exist.")
    else:
        print("Usage: python HealthBI.py file")
