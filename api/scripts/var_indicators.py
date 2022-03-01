import json
from unicodedata import category
from pandas import *
from .shape_csv import get_csv_cols

class VarCategory:
    def __init__(self, category_name):
        self.category_uid = None #created after insertion to POSTGRES
        self.category_name = category_name

class VarTopic(VarCategory):
    def __init__(self, category_name, topic_name):
        super().__init__(category_name)
        self.topic_uid = None #created after insertion to POSTGRES
        self.topic_name = topic_name

class VarIndicator(VarTopic):
    def __init__(self, category_name, topic_name, indicator_name, indicator_unit):
        super().__init__(category_name, topic_name)
        self.indicator_uid = None #created after insertion to POSTGRES
        self.indicator_name = indicator_name
        self.indicator_unit = indicator_unit

    def __eq__(self, other):
             if self.category_name ==other.category_name and self.topic_name==other.topic_name and self.indicator_name==other.indicator_name:
                  return True
             else:
                  return False

    def 
