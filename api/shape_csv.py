#!/usr/bin/python
import csv, json
from types import NoneType
from pandas import *
import sys, os

from api.scripts.var_indicator import Categories, IndicatorController, Topics, Indicators
from api.scripts.dim_temporal import DimTemporal
from api.scripts.dim_location import DimLocation
# from .dimScripts.var_indicator import VarIndicator
# from .dimScripts.fact_indicators import FactIndicator

class ShapeCSV:
    """
    Takes in csv and fits columns and data to the data model.
    """
    def __init__(self, csv_file, mapping_json):
        self.csv_file = csv_file
        self.mapping_json = mapping_json
        self.csv_columns = []
        #self.fact_indicator_objs = []
        # Initiate dimension objects. These store the list of objects.
        self.dim_temporal = DimTemporal(self.mapping_json)
        self.dim_location = DimLocation(self.mapping_json)
        self.var_category_objs = None
        self.var_topic_objs = None
        self.var_indicator_objs = Indicators()
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
        ### check if indicators is in column headers based on dictionary mapping
        if self.mapping["Var_Indicators_Format"] == "Column_Header":
            print("Indicators' names are in column headers.")
            mapping = self.mapping
            self.var_category_objs, self.var_topic_objs, self.var_indicator_objs = IndicatorController().create_var_indicator_with_mapping(mapping)
        with open(self.csv_file, mode='r', encoding="utf-8-sig") as csv_file:
            '''
            # Get json values for temporal, location, indicator, and fact_indicator.
            dim_temporal_json, dim_is_value = self.dim_temporal.get_json_cols()
            dim_location_json = self.dim_location.get_json_cols()
            if dim_is_value:
                self.dim_temporal.create_new_temporal_object(dim_temporal_json)
            '''
            # READ CSV
            # Start at the first row of data
            csv_reader = csv.DictReader(csv_file)
            line_count = 1
            for row in csv_reader:
                '''
                if dim_is_value == False:
                    # TEMPORAL
                    temporal_val = self.dim_temporal.get_csv_val(row, dim_temporal_json)
                    self.dim_temporal.create_new_temporal_object(temporal_val)
                # LOCATION
                location_vals = self.dim_location.get_csv_val(row, dim_location_json)
                self.dim_location.create_new_location_object(location_vals)
                '''
                line_count += 1
            # print(self.dim_location.location_vals)
            print(f'Processed {line_count} lines.\n')
        # print(f'dim_temporal_objs: {self.dim_temporal.temporal_objs}\n')