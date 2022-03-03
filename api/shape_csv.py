#!/usr/bin/python
import csv
from pandas import *
from .scripts.dim_temporal import DimTemporal
from .dimScripts.dim_location import DimLocation
# from .dimScripts.var_indicator import VarIndicator
# from .dimScripts.fact_indicators import FactIndicator

class ShapeCSV:
    """
    Takes in csv and fits columns and data to the data model.
    """
    def __init__(self, csv_file, json_file):
        self.csv_file = csv_file
        self.json_file = json_file
        self.csv_columns = []
        self.dim_location_objs = []
        self.var_indicator_objs = []
        self.fact_indicator_objs = []
        # Initiate dimension objects. These store the list of objects.
        self.dim_temporal = DimTemporal(self.json_file)

    def run_shaping(self):
        """
        Parses the csv for wanted Temporal, Location, Indicator, Fact_Indicator columns. 
        Creates objects for all unique columns.
        """
        # Get columns of CSV
        self.get_csv_cols()
        # print(self.csv_columns)
        self.parse_csv_for_objects()

    def get_csv_cols(self):
        with open(self.csv_file, mode='r', encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    self.csv_columns.append(f'{", ".join(row)}')
                    break

    def parse_csv_for_objects(self):
        with open(self.csv_file, mode='r', encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # Get json values for temporal, location, indicator, and fact_indicator.
            dim_temporal_json, dim_is_value = self.dim_temporal.get_json_cols()
            if dim_is_value:
                self.dim_temporal.create_new_temporal_object(dim_temporal_json)
            # Start at the first row of data
            line_count = 1
            for row in csv_reader:
                if dim_is_value == False:
                    self.temporal_val = self.dim_temporal.get_csv_val(row, dim_temporal_json)
                    # Create new temporal object if unique.
                    self.dim_temporal.create_new_temporal_object(self.temporal_val)
                line_count += 1
            print(f'Processed {line_count} lines.\n')
        # print(f'dim_temporal_objs: {self.dim_temporal.temporal_objs}\n')

    # def addVarIndicator(self, indicator):
    #     for i in self.var_indicators:
    #         if i == indicator:
    #             print("This indicator already exists in this database.")
    #         else:    
    #             self.var_indicators.append(indicator)
    #             print("A new indicator: %s has been added." % (indicator.indicator_name))
    #     return True

    # def createFact(self):
    #     #column
    #     self.dim_temporal = DimTemporal().temporal_vals

    #     # row by row
    #     temp = self.temporals.addTemporal(Temporal(temporal))
    #     # returns a loc inside the list of location objects
    #     loc = self.locations.addLocation(Location('US', 'AL', 'City')) #do not add if already exist

    #     fact_indicator = FactIndicator(temporal, loc, indicator, data)
    #     pass