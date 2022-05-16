#!/usr/bin/python
import csv, json
from pandas import *
from api.scripts.var_indicator import Categories, IndicatorController, Topics, Indicators
from api.scripts.dim_temporal import DimTemporal
from api.scripts.dim_location import DimLocation
# from .dimScripts.var_indicator import VarIndicator
# from .dimScripts.fact_indicators import FactIndicator

class ShapeCSV:
    """
    Takes in csv and fits columns and data to the data model.
    This class holds the dim_temporal, dim_location, var_indicator, fact_indicator classes which hold the objects.
    """
    def __init__(self, csv_file, mapping_json):
        self.csv_file = csv_file
        self.mapping_json = mapping_json
        self.csv_columns = []
        # Initiate dimension objects. These store the list of objects.
        self.dim_temporal_objs = DimTemporal()
        # self.dim_location_objs = DimLocation(self.mapping_json)
        self.var_category_objs = None
        self.var_topic_objs = None
        self.var_indicator_objs = None
        self.mapping = self.getMapping(mapping_json)

    def run_shaping(self):
        """
        Parses the csv for wanted Temporal, Location, Indicator, Fact_Indicator columns. 
        Creates objects for all unique columns.
        """
        # Get columns of CSV
        self.get_csv_cols()
        self.parse_csv_for_objects()

    def get_csv_cols(self):
        """
        Only reads in first line of csv for the column names.
        """
        with open(self.csv_file, mode='r', encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    self.csv_columns.append(f'{", ".join(row)}')
                    break

    def getMapping(self, json_file):
        with open(json_file) as f:
            dictData = json.load(f)
        return dictData
    
    def parse_csv_for_objects(self):
        mapping = self.mapping
        ### Add indicators in column headers
        ### check if indicators is in column headers based on dictionary mapping
        # if mapping["Var_Indicators_Format"] == "Column_Header":
        #     print("Indicators' names are in column headers.")
        #     self.var_category_objs, self.var_topic_objs, self.var_indicator_objs = IndicatorController().create_var_indicator_with_mapping(mapping)

        if mapping["Temporal_UID"]["value"] != "" and self.mapping["Temporal_UID"]["column_name"] == "":
            self.dim_temporal_objs.create_new_temporal_object("value", mapping["Temporal_UID"]["value"])
        
        with open(self.csv_file, mode='r', encoding="utf-8-sig") as csv_file:
            # Get json values for temporal, location, indicator, and fact_indicator.
            # dim_location_json = self.dim_location_objs.get_json_cols()
            # READ CSV
            # Start at the first row of data
            csv_reader = csv.DictReader(csv_file)
            line_count = 1
            for row in csv_reader:
                # TEMPORAL
                if mapping["Temporal_UID"]["column_name"]:
                    self.dim_temporal_objs.create_new_temporal_object("column_name", mapping["Temporal_UID"]["column_name"], row)
                # LOCATION
        #         #location_vals = self.dim_location.get_csv_val(row, dim_location_json)
        #         # self.dim_location_objs.create_new_location_object(row, dim_location_json)
                line_count += 1
            # print(self.dim_location_objs.locations)
            print(f'Processed {line_count} lines.\n')
        # print(f'dim_temporal_objs: {self.dim_temporal.temporal_objs}\n')