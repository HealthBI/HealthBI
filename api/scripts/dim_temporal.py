#!/usr/bin/python
import re
from pandas import *

class Temporal:
    """
    Temporal Object.
    The temporal_uid is required to be in format (year, month, date) 00000000.
    If not given a temporal value, the user can give one column name in the dataset
    that represents the temporal value.
    """
    def __init__(self, uid, year, month_99, month_xxx, month_name, month_xxx_year, day_99, day_month_xxx_year, dayofweek_xxx=None, quarter_q9=None, quarter_q9_year=None, season=None):
        self.temporal_uid = uid
        # Possible temporal value.
        self.year = year
        self.month_99 = month_99
        self.month_xxx = month_xxx
        self.month_name = month_name
        self.month_xxx_year = month_xxx_year
        self.day_99 = day_99
        self.day_month_xxx_year = day_month_xxx_year
        self.dayofweek_xxx = dayofweek_xxx
        self.quarter_q9 = quarter_q9
        self.quarter_q9_year = quarter_q9_year
        self.season = season

    def __eq__(self, other):
        if (self.temporal_uid==other.temporal_uid and
            self.year==other.year and 
            self.month_99==other.month_99 and 
            self.month_xxx==other.month_xxx and 
            self.month_name==other.month_name and
            self.month_xxx_year == other.month_xxx_year and
            self.day_99 == other.day_99 and
            self.day_month_xxx_year == other.day_month_xxx_year and 
            self.dayofweek_xxx == other.dayofweek_xxx and 
            self.quarter_q9 == other.quarter_q9 and 
            self.quarter_q9_year == other.quarter_q9_year and
            self.season == other.season):
            return True
        else:
            return False

class DimTemporal():
    """
    Shapes csv dim_temporal columns.
    """
    def __init__(self):
        self.temporals = []
        self.num_of_temporals = 0

    def get_csv_val(self, row, json_col):
        """
        This is only called if column_name was given in json.
        Gets the year value in row.
        """
        for key in row:
            if key in json_col:
                return row[key]
        return

    def create_temporal_uid(self, year, month, day):
        """
        Creates temporal_uid. Mask to correct number of digits, year, month, and day (bigint). 
        Note: Uniqueness is not checked here. All objects are created.
        """
        uid = int(year + month + day)
        return uid

    def extract_temporal_value(self, value):
        year = value[0:4]
        month = value[4:6]
        month_name = None
        month_xxx = None
        month_xxx_year = None 
        day = value[6:9]
        if month == '01':
            month_name = "Januaury"
            month_xxx = "Jan"
        elif month == '02':
            month_name = "February"
            month_xxx = "Feb"
        elif month == '03':
            month_name = "March"
            month_xxx = "Mer"
        elif month == '04':
            month_name = "April"
            month_xxx = "Apr"
        elif month == '05':
            month_name = "May"  
            month_xxx = "May"
        elif month == '06':
            month_name = "June"
            month_xxx = "Jun"  
        elif month == '07':
            month_name = "July"
            month_xxx = "Jul"  
        elif month == '08':
            month_name = "August"
            month_xxx = "Aug"  
        elif month == '09':
            month_name = "September"
            month_xxx = "Sep"  
        elif month == '10':
            month_name = "October"
            month_xxx = "Oct"  
        elif month == '11':
            month_name = "November"  
            month_xxx = "Nov"
        elif month == '12':
            month_name = "December"  
            month_xxx = "Dec"
        if month_xxx != None:
            month_xxx_year = month_xxx + year
        return year, month, month_name, month_xxx, month_xxx_year, day

    def create_new_temporal_object(self, tem_type, value, row=None):
        """
        Create a new temporal object.
        """
        found = False
        if tem_type == "value":
            year, month_99, month_name, month_xxx, month_xxx_year, day_99 = self.extract_temporal_value(value)
            day_month_xxx_year = None
            temp = Temporal(value, year, month_99, month_xxx, month_name, month_xxx_year, day_99, day_month_xxx_year)
            self.temporals.append(temp)
            return temp
        if tem_type == "column_name":
            if re.search("year", value):
                year = row[value]
                uid = self.create_temporal_uid(year, "00", "00")
            else:
                year = None
            month_99 = None
            month_name = None
            day_99 = None
            month_xxx = None
            month_xxx_year = None
            day_month_xxx_year = None
            temp = Temporal(uid, year, month_99, month_xxx, month_name, month_xxx_year, day_99, day_month_xxx_year)
            if self.num_of_temporals == 0:
                self.temporals.append(temp)
                self.num_of_temporals += 1
                print("A new temp has been created: %s" % row[value])
                return self.temporals[-1]
            else:
                for i in range(self.num_of_temporals):
                    if self.temporals[i] == temp:
                        found = True
                        print("This temp %s was already read in this csv." % row[value])
                        return self.temporals[i]
                if not found:
                    self.temporals.append(temp)
                    self.num_of_temporals += 1
                    print("A new temp has been created: %s" % row[value])
                    return self.temporals[-1]
                