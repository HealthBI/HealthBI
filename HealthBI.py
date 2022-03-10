#!/usr/bin/python
import os
import sys
import psycopg2
from api.shape_csv import ShapeCSV
from api.inject_csv import InjectCSV

class HealthBI:
    """
    HealthBI.py takes in a csv file as an argument and shapes it to fit the data model.
    This class acts as the Data Controller. 
    """
    def __init__(self, csv_file, json_file):
        self.csv_file = csv_file
        self.json_file = json_file
        self.inject = None
        # Connect to database.
        self.conn, self.cursor = self.connect_to_database()
        # Run shaping.
        self.shape = None
        self.shape_csv()
        self.inject_shaped_csv()
        print("Data successfully processed.\n")
        self.conn.close()
    
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
    
    def shape_csv(self):
        """
        Data gets shaped to fit the data model.
        """
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