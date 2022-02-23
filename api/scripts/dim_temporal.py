from http.client import CONFLICT
from re import T
from matplotlib.pyplot import table
import psycopg2, csv
import json
from datetime import datetime

'''
cur.execute(
    """
    CREATE TABLE DIM_TEMPORAL (
    Temporal_UID bigint  NOT NULL,
    Year varchar(128)  NOT NULL,
    Month_99 varchar(128)  NOT NULL,
    Month_XXX varchar(128)  NOT NULL,
    Month_Name varchar(128)  NOT NULL,
    Month_XXX_Year varchar(128)  NOT NULL,
    Day_99 varchar(128)  NOT NULL,
    Day_Month_XXX_Year varchar(128)  NOT NULL,
    DayOfWeek_XXX varchar(128)  NULL,
    Quarter_Q9 varchar(128)  NULL,
    Quarter_Q9_Year varchar(128)  NULL,
    Season varchar(128)  NULL,
    CONSTRAINT Temporal_UID PRIMARY KEY (Temporal_UID)
    );
    """
)
insert_query_na = "INSERT INTO dim_temporal VALUES (-1, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA');"
cur.execute(insert_query_na)
conn.commit()

cur.execute("SELECT * from dim_temporal;")
all = cur.fetchall()
print(all)
'''
def validate(date_text):
    for fmt in ('%Y', '%Y%m', '%Y%m%d'):
        try:
            return datetime.strptime(date_text, fmt)
        except ValueError:
            pass
    return False

def user_dictionary(filename):
    list_of_column_names = []
    data_model_dict = { "DataSet_Name":"",
                        "DataFile_Name": "",
                        "Temporal_UID": {"column_name": "", "value": ""},
                        "Location": [
                            {"Country_Name": "", "Region_Name": "", "Division_Name": "", "State_Name": "",
                            "County_Name": "", "City_Name": "","Town_Name": "", "Neighborhood_Name": ""}
                        ],
                        "Categories": "",
                        "Topics": "",
                        "Indicators": [
                            {"Indicator_Name": "", "Indicator_Unit": ""}
                        ]}

    with open(filename, 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            # adding the first row
            list_of_column_names.append(row)
            # breaking the loop after the
            # first iteration itself
    print('List of column names : ', list_of_column_names[0])
    temporal_uid = input("Enter temporal column:") #Ask user for temporal column name
    data_model_dict["Temporal_UID"] = temporal_uid #Update temporal column
    return data_model_dict

def parse_data(filename, data_model_dict):
    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
    cur = conn.cursor()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        temporal = data_model_dict["Temporal_UID"]
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
    data_model_dict = user_dictionary("temporal_test.csv")
    parse_data("temporal_test.csv", data_model_dict)
#parse_data("temporal_test.csv")