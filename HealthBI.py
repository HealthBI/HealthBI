#!/usr/bin/python
import os
import sys
import psycopg2
from api.scripts.shape_csv import ShapeCSV

class HealthBI:
    """
    HealthBI.py takes in a csv file as an argument and shapes it to fit the data model.
    """
    def __init__(self, csv_file, json_file):
        self.csv_file = csv_file
        self.json_file = json_file
        self.conn, self.cursor = self.connect_to_database()
        status = self.shape_csv()
        if status == True:
            print("Data successfully processed.")
        else:
            print("Data failed processed.")
        self.conn.close()
    
    def connect_to_database(self):
        conn = psycopg2.connect(
                    database="HealthBI", 
                    user="postgres"
        )
        cursor = conn.cursor()
        cursor.execute("select version()")
        data = cursor.fetchone()
        print("Connection established to: ",data)
        return conn, cursor
    
    def shape_csv(self):
        shape = ShapeCSV(self.csv_file, self.json_file, self.conn, self.cursor)
        status = shape.run_shaping()
        return status

if __name__=="__main__":
    if len(sys.argv) == 3:
        csv_exists = os.path.exists(sys.argv[1])
        json_exists = os.path.exists(sys.argv[2])
        if csv_exists == True and json_exists == True:
            run = HealthBI(sys.argv[1], sys.argv[2])
        elif csv_exists == False:
            print("CSV file does not exist.")
        elif json_exists == False:
            print("JSON file does not exist.")
    else:
        print("Usage: python HealthBI.py csvFile jsonFile")
