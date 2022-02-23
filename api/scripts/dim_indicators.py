from http.client import CONFLICT
from re import T
from unicodedata import category
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
    category = healthBI_mapping["Categories"][0]["Category"]
    cur.execute("INSERT INTO var_category (category_name) VALUES ('{}')".format(category))
    conn.commit()

if __name__ == "__main__":
    healthBI_mapping = user_dictionary("./api/scripts/mapping.json") 
    print(healthBI_mapping)
    parse_data("indicator_column_test.csv", healthBI_mapping)
#parse_data("temporal_test.csv")