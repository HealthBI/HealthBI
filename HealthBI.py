#!/usr/bin/python3
'''
    Drexel University CCI Senior Project 2022
    HealthBI
    Contributors:
    Corinna Hoang
    Trang Hoang 
    Chris Lynch 
    Charles Porter 
    Angie Margai-Ren
'''
import csv
import os
import re
import sys
import psycopg2
from api.shape_csv import ShapeCSV
from api.inject_csv import InjectCSV

class HealthBI:
    """
    HealthBI.py is the main object of the HealthBI API. 
    API functionality includes:
    - upload_dataset
    - view_all_datasets
    - correlate_dataset
    - select
    """
    def __init__(self):
        self.csv_file = None
        self.json_file = None
        self.inject = None
        self.shape = None
    
    def connect_to_database(self):
        """
        Connection to database happens once. The conn and curser is passed into and used by the other objects.
        """
        conn = psycopg2.connect(
                    database="healthbi", 
                    user="postgres",
                    host="localhost"
        )
        cursor = conn.cursor()
        cursor.execute("select version()")
        data = cursor.fetchone()
        print("Connection established to: {}.\n".format(data))
        return conn, cursor

    def shape_csv(self, csv_file=None, json_file=None):
        """
        Data gets shaped to fit the data model.
        """
        self.csv_file = csv_file
        self.json_file = json_file
        self.shape = ShapeCSV(self.csv_file, self.json_file)
        self.shape.run_shaping()
        return

    def inject_shaped_csv(self):
        """
        Injects the new unique objects the database.
        """
        self.inject = InjectCSV(self.conn, self.cursor, self.shape)
        self.inject.run_injection()
        return

    def upload_dataset(self, csv_file, json_file):
        self.csv_file = csv_file
        self.json_file = json_file
        # Connect to database.
        self.conn, self.cursor = self.connect_to_database()
        self.shape_csv()
        self.inject_shaped_csv()
        print("Data successfully processed.\n")
        self.conn.close()

    def view_all_datasets(self):
        pass

    def correlate_dataset(self):
        pass

    def select(self):
        pass

#     def apicmds(self, cmd):
#         """
#         API command options:
#         Help, Correlate, Select, Insert
#         """
#         if re.match('help', cmd, re.IGNORECASE):
#             print("HealthBI Commands:\n")
#             print("help\n")
#             print("correlate temporal location indicators\n")
#             print("insert csvFile jsonFile\n")
#             print("select table\n")
#         elif re.match('correlate', cmd, re.IGNORECASE):
#             print("Correlating...")
#         elif re.match('insert', cmd, re.IGNORECASE):
#             print("Inserting dataset...")

# if __name__=="__main__":

#     healthbi = HealthBI()

#     if len(sys.argv) == 2:
#         run = healthbi.apicmds(sys.argv[1])
#     elif len(sys.argv) == 4:
#         run = healthbi.apicmds(sys.argv[1])
#         csv_exists = os.path.exists(sys.argv[2])
#         json_exists = os.path.exists(sys.argv[3])
#         if csv_exists == True and json_exists == True:
#             run = HealthBI(sys.argv[1], sys.argv[2])
#         elif csv_exists == False:
#             print("CSV file does not exist.")
#         elif json_exists == False:
#             print("JSON file does not exist.")
#     else:
#         print("Usage: python HealthBI.py csvFile jsonFile")