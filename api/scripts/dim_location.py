import json
from pandas import *
class DimLocation():
    """
    Shapes csv dim_location columns.
    """
    def __init__(self, csv_file, json_file, db_conn, db_cur):
        self.csv_file = csv_file
        self.json_file = json_file
        self.db_conn = db_conn
        self.db_cur = db_cur
        self.json_location_cols = []
        self.location_vals = {}

    def get_json_cols(self):
        """
        Get all json cols for location. Based off known required data model fields.
        Location columns: "Location": [
        {"Country_Name": "", "Region_Name": "", "Division_Name": "", "State_Name": "",
        "County_Name": "", "City_Name": "city","Town_Name": "", "Neighborhood_Name": ""}],
        returns list of unique location combinations
        """
        with open(self.json_file) as json_file:
            dictData = json.load(json_file)
            for x in dictData['Location']:
                for val in x:
                    self.json_location_cols.append(x[val])
        # Remove duplicate values in list
        for i in self.json_location_cols:
            print(i)
            tmp = []
            [tmp.append(x) for x in self.json_location_cols if x not in tmp and x]
        self.json_location_cols = tmp
        return self.json_location_cols
    
    def do_data_injection(self):
        """
        For every location value, look for the unique row values and insert with new unique id.
        """
        #TODO: create unique location id
        sql = "INSERT INTO dim_temporal VALUES ('5', %s, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA')"
        col_name = self.json_location_cols[0]
        all_vals = self.location_vals.get(col_name)
        self.db_cur.execute(sql, [all_vals])
        self.db_conn.commit()
        print(self.db_cur.rowcount, "records inserted.")

        self.db_cur.execute("select * from dim_temporal")
        result = self.db_cur.fetchall()
        print(result)