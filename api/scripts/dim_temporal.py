from http.client import CONFLICT
from re import T
from matplotlib.pyplot import table
import psycopg2, csv
import json
from datetime import datetime
from api.scripts.shape_csv import ShapeCSV

class dim_temporal(ShapeCSV):
    """
    Shapes csv dim_temporal columns.
    """
    def __init__(self, csv_file):
        super().__init__(csv_file)
        self.csvAsDict(self.csv_file)
        # data_model_dict = self.user_dictionary("temporal_test.csv")
        # self.parse_data("temporal_test.csv", data_model_dict)

    def validate(self,date_text):
        for fmt in ('%Y', '%Y%m', '%Y%m%d'):
            try:
                return datetime.strptime(date_text, fmt)
            except ValueError:
                pass
        return False

    def prompt_temporal(self):
        print('List of column names : ', self.cvs_columns[0])
        temporal_uid = input("Enter temporal column:") #Ask user for temporal column name
        self.req_data_model_dict["Temporal_UID"] = temporal_uid #Update temporal column

    def parse_data(self,filename, data_model_dict):
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

    # TODO: create new object for every new temporal object (1. 2021, 2. 2022)