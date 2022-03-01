from ast import ImportFrom
import csv

from api.scripts.fact_indicators import FactIndicator
from .dim_temporal import DimTemporal
from .dim_location import DimLocation, Location
from .var_indicators import VarIndicator
import posgresql

class ShapeCSV:
    '''
    temporals = []
    locations = []
    indicators = []
    facts = []
    row by row
        temp = temporals.append(temporal)
        loc = locations.append(location)
        indi = indicators.append(indicator)
        fact = facts.append(fact_ind(temp, loc, indi, val))
    done reading csv
    inject(temporals) -> update each temp.uid
    inject(locations) -> update each loc.uid
    inject(indicators) -> update each indi.uid
    inject(fact) -> 
    '''

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
        self.var_indicators = []
        self.dim_temporal = DimTemporal().temporal_vals
        # Get columns of CSV
        self.get_csv_cols()
        # Initialize required fields
        # self.dim_temporal = DimTemporal(self.csv_file, self.json_file, self.db_conn, self.db_cur)
        self.dim_location = DimLocation(self.csv_file, self.json_file, self.db_conn, self.db_cur)

    def get_csv_row(self, column_name):
        
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


    def compare_csv_to_json(self):
        """
        Check if existing columns from csv are in required columns from json.
        """
        # Get desired temporal cols from json, get vals from cols in csv
        # temp_json_cols = self.dim_temporal.get_json_cols()
        # # if column_name was given, look for values, if not do injection with given value
        # if temp_json_cols[0] != '':
        #     self.dim_temporal.get_csv_vals(temp_json_cols)
        # elif temp_json_cols[1] != '':
        #     self.dim_temporal.do_value_injection(temp_json_cols[1])
        # Get desired location cols from json, get vals from cols in csv
        loc_json_cols = self.dim_location.get_json_cols()
        return True 

    def addVarIndicator(self, indicator):
        for i in self.var_indicators:
            if i == indicator:
                print("This indicator already exists in this database.")
            else:    
                self.var_indicators.append(indicator)
                print("A new indicator: %s has been added." % (indicator.indicator_name))
        return True

    def createFact(self):
        #column
        self.dim_temporal = DimTemporal().temporal_vals

        # row by row
        temp = self.temporals.addTemporal(Temporal(temporal))
        # returns a loc inside the list of location objects
        loc = self.locations.addLocation(Location('US', 'AL', 'City')) #do not add if already exist

        fact_indicator = FactIndicator(temporal, loc, indicator, data)
        pass

    def run_injections(self):
        # self.dim_temporal.do_data_injection()
        # upon finishing reading csv completely
        # indicator object list injection
        for indicator in self.var_indicators:
            indicator.indicator_uid = insertIndicatorToDB(indicator)
        # location object list injection
        # temporal object list injection

        return True

    
    def run_shaping(self):
        """
        Gets the correct colomns needed for dim_temporal, dim_location, and fact_indicator.
        """
        status = self.compare_csv_to_json()
        status = self.run_injections()
        return status