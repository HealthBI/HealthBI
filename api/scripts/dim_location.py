#!/usr/bin/python
from distutils.command import check
import json
from numpy import full
from pandas import *

class Location:
    """
    Location Object
    """
    def __init__(self, country_name, region_name, devision_name, state_name, county_name, city_name, town_name, neighborhoood_name, location_uid=None):
        self.uid = location_uid
        self.country_name = country_name
        self.region_name = region_name
        self.devision_name = devision_name
        self.state_name = state_name
        self.county_name = county_name
        self.city_name = city_name
        self.town_name = town_name
        self.neighborhood_name = neighborhoood_name

    def __eq__(self, other):
        if self.country_name==other.country_name and self.region_name==other.region_name and self.devision_name==other.devision_name and self.state_name==other.state_name and self.county_name==other.county_name and self.city_name==other.city_name and self.town_name==other.town_name and self.neighborhood_name==other.neighborhood_name:
            return True
        else:
            return False


class DimLocation():
    """
    Shapes csv dim_location columns.
    """
    def __init__(self, json_file):
        self.json_file = json_file
        self.json_location_cols = {}
        self.location_vals = []
        self.locations = []

    def get_json_cols(self):
        """
        Get all json cols for location. Based off known required data model fields.
        Location columns: "Location": [
        {"Country_Name": "", "Region_Name": "", "Division_Name": "", "State_Name": "",
        "County_Name": "", "City_Name": "", "Town_Name": "", "Neighborhood_Name": ""}],
        returns list of unique location combinations
        Check for uniqueness in the countryname stateaname countyname skip region and division, 
        search if record with all value exists. Finish return with location uid, insert will return location uid
        """
        with open(self.json_file) as json_file:
            dictData = json.load(json_file)
            for loc in dictData['Location']:
                for val in loc:
                    if loc[val] != '':
                        self.json_location_cols[val] = loc[val]
                    else:
                        # All keys in location that don't have a value will be set to None
                        self.json_location_cols[val] = ''
        return self.json_location_cols

    def get_csv_val(self, row, json_col):
        """
        Reads a row to check if the combination of rows are unique.
        For every row, save valid json keys and row value to dictionary.
        """
        pairs = {}
        for key in row:
            for i in self.json_location_cols:
                if self.json_location_cols[i] in row and self.json_location_cols[i] == key:
                    if self.json_location_cols[i] not in pairs:
                        # print("key:", i)
                        # print("value:", row[key])
                        pairs[i] = row[key]
                else:
                    pairs[i] = ''
        self.location_vals.append(pairs)
        return pairs

    def dict_compare(self, d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        shared_keys = d1_keys.intersection(d2_keys)
        same = set(o for o in shared_keys if d1[o] == d2[o])
        return same

    def create_new_location_object(self, row, values):
        """
        Create a new location object if unique value. Not given a location_uid.
        """
        found = False
        loc = Location(row[values["Country_Name"]], row[values["Region_Name"]], values["Division_Name"], values["State_Name"], values["County_Name"], row[values["City_Name"]], values["Town_Name"], values["Neighborhood_Name"])
        if len(self.locations) == 0:
            self.locations.append(loc)
        else:
            for i in self.locations:
                if loc == i:
                    found = True
                    print("Location already existed ", values)
            if not found:
                self.locations.append(loc)
        #print(len(self.locations))
        return