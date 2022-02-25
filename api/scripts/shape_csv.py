import csv
from .dim_temporal import DimTemporal

class ShapeCSV:
    """
    Takes in csv and fits columns and data to the data model.
    """
    def __init__(self, csv_file, json_file, db_conn, db_cursor):
        self.csv_file = csv_file
        self.json_file = json_file
        self.db_conn = db_conn
        self.db_cur = db_cursor
        self.cvs_columns = []
        self.json_columns = []

        # Get columns of CSV
        self.get_csv_cols()
        # Initialize required fields
        self.dim_temporal = DimTemporal(self.csv_file, self.json_file, self.db_conn, self.db_cur)

    def get_csv_cols(self):
        with open(self.csv_file, mode='r', encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    self.cvs_columns.append(f'{", ".join(row)}')
                    break
                    # line_count += 1
                # line_count += 1
            # print(f'Processed {line_count} lines.')
            # print(f'Column names: {self.cvs_columns}')

    def run_shaping(self):
        """
        Gets the correct colomns needed for dim_temporal, dim_location, and fact_indicator.
        """
        status = self.compare_csv_to_json()
        status = self.run_injections()
        return status

    def compare_csv_to_json(self):
        """
        Check if existing columns from csv are in required columns from json.
        """
        # Get desired temporal cols from json, get vals from cols in csv
        temp_json_cols = self.dim_temporal.get_json_cols()
        # if column_name was given, look for values, if not do injection with given value
        if temp_json_cols[0] != '':
            self.dim_temporal.get_csv_vals(temp_json_cols)
        return True 

    def run_injections(self):
        self.dim_temporal.do_data_injection()
        return True

    def createFact(self):
        pass