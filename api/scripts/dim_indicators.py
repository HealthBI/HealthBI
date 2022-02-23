from http.client import CONFLICT
from re import T
from matplotlib.pyplot import table
import psycopg2, csv
import json
from datetime import datetime

def validate(date_text):
    return True

def user_dictionary(filename):
    # Opening JSON file
    f = open(filename)
    data = json.load(f)
    jtopy=json.dumps(data) #json.dumps take a dictionary as input and returns a string as output.

    # returns JSON object as
    # a dictionary
    data_model_dict = json.loads(jtopy)
    
    # Closing file
    f.close()

    return data_model_dict

def parse_data(filename, healthBI_mapping):
    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
    cur = conn.cursor()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        temporal = healthBI_mapping["Temporal_UID"]
        i = 1 #row count
        for row in reader:
            # Check format of temporal input is of format YYYY, YYYYMM, or YYYYMMDD 
            if not validate(row[temporal]):
                print("Your temporal data at row %s as: %s" % (i, row[temporal]))
                print("Incorrect data format, should be YYYY, or YYYYMM, or YYYYMMDD")
                # 10000 record of incorrect data format echoed to a separate csv
            else:
                # TODO: Automate other columns, such as year, month, date
                # adding temporal value directly as primary keys
                year = row[temporal][0:4]
                #month = row[temporal][4:6] if len(row[temporal]) >= 6 else 'NA'
                #day = row[temporal][6:8] if len(row[temporal]) >= 8 else 'NA'
                cur.execute("INSERT INTO dim_temporal VALUES {}".format("(%s, \
                                %s, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA') \
                                ON CONFLICT (Temporal_UID) DO NOTHING;" % (row[temporal], year)))
            i += 1
    conn.commit()

if __name__ == "__main__":
    healthBI_mapping = user_dictionary("./api/scripts/healthBImapping.json") 
    print(healthBI_mapping)
    parse_data("indicator_column_test.csv", healthBI_mapping)
#parse_data("temporal_test.csv")