#!/usr/bin/python
from ast import Return
import re
import numpy as np

from matplotlib.pyplot import get

#from scripts.dim_location import DimLocation
#from scripts.dim_temporal import DimTemporal
#from scripts.var_indicator import Indicators

from psycopg2.extensions import AsIs

class InjectCSV():
    def __init__(self, conn, cursor, shape):
        self.conn = conn
        self.curr = cursor
        #self.dim_temporal_objs = shape.dim_temporal_objs
        self.temporals = shape.dim_temporal_objs.temporals
        self.locations = shape.dim_location_objs.locations
        self.categories = shape.var_category_objs.categories
        self.topics = shape.var_topic_objs.topics
        self.indicators = shape.var_indicator_objs.indicators
    def run_injection(self):
        """
        For every object, give it a unique id and inject into HealthBI database.
        """
        self.insert_temporals()
        self.insert_locations()
        self.insert_categories()
        self.insert_topics()
        self.insert_indicators()

    def get_temporal_info(self, tem_value):
        """
        Breaks up the given temporal value to get uid and value.
        """
        uid = getattr(tem_value, "temporal_uid")
        value = getattr(tem_value, "temp_value")
        #year = tem_value[0:4]
        #month = tem_value[4:5]
        #day = tem_value[6:7]
        return uid, value

    def insert_temporals(self):
        print("INSERTING temporals...")
        if len(self.temporals) == 1:
            uid, value = self.get_temporal_info(self.temporals[0])
            sql = ("INSERT INTO dim_temporal VALUES ('{}', '{}', '{}', '{}') \
                        ON CONFLICT(temporal_uid) \
                        DO UPDATE SET temporal_uid=EXCLUDED.temporal_uid \
                        RETURNING temporal_uid".format(uid, value[0:4], value[4:6], value[6:8]))
            self.curr.execute(sql)
        else:
            for temp in self.temporals:
                sql = ("INSERT INTO dim_temporal VALUES ('{}', '{}', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA') \
                        ON CONFLICT(temporal_uid) \
                        DO UPDATE SET temporal_uid=EXCLUDED.temporal_uid \
                        RETURNING temporal_uid".format(temp.temporal_uid, temp.year))
                self.curr.execute(sql)
        self.conn.commit()
        return

    def insert_locations(self):
        for location in self.locations:
            sql = ("INSERT INTO dim_location (country_name, region_name, division_name, state_name, county_name, city_name, town_name, neighborhood_name) \
                    VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') \
                    ON CONFLICT (location_uid) \
                    DO UPDATE SET location_uid = EXCLUDED.location_uid \
                    RETURNING location_uid;".format(location.country_name, location.region_name, location.division_name, location.state_name, location.county_name, location.city_name, location.town_name, location.neighborhood_name))
            self.curr.execute(sql)

            try:
                location.location_uid = self.curr.fetchone()[0]
                self.conn.commit()
                print(self.curr.rowcount, "locations records inserted.")
            except:
                print("Location %s already exists" % location.location_uid)
            self.conn.commit()
        return

    def insert_categories(self):
        print("INSERTING categories...")
        for category in self.categories:
            # return the id of inserted category in postgres
            # if category already existed return its id
            sql = ("INSERT INTO var_category (category_name) VALUES ('{}') \
                    ON CONFLICT(category_name) \
                    DO UPDATE SET category_name=EXCLUDED.category_name \
                    RETURNING category_uid".format(category.category_name))
            self.curr.execute(sql)
            try:
                category.category_uid = self.curr.fetchone()[0]
                print(category.category_uid)
                print(self.curr.rowcount, "category records inserted.")
            except:
                #TODO: let users know that category object already existed already
                print("Category %s already existed" % category.category_name)
            self.conn.commit()
        return

    def insert_topics(self):
        print("INSERTING topics...")
        for topic in self.topics:
            # return the id of inserted topic in postgres
            # if topic already existed return its id
            sql = ("INSERT INTO var_topic (category_uid, topic_name) VALUES ('{}', '{}') \
                    ON CONFLICT (category_uid, topic_name) \
                    DO UPDATE SET topic_name=EXCLUDED.topic_name \
                    RETURNING topic_uid;".format(topic.category.category_uid, topic.topic_name))
            self.curr.execute(sql)
            try:
                topic.topic_uid = self.curr.fetchone()[0]
                print(topic.topic_uid)
                self.conn.commit()
                print(self.curr.rowcount, "topic records inserted %s." % topic.topic_name)
            except:
                print("Topic %s already existed" % topic.topic_name)
            self.conn.commit()
        return

    def insert_indicators(self):
        print("INSERTING indicators...")
        for indicator in self.indicators:
            # return the id of inserted topic in postgres
            # if topic already existed return its id
            sql = ("INSERT INTO var_indicator (topic_uid, indicator_name, indicator_unit) VALUES ('{}', '{}', '{}') \
                    ON CONFLICT (topic_uid, indicator_name) \
                    DO UPDATE SET indicator_unit=EXCLUDED.indicator_unit, \
                                  indicator_name=EXCLUDED.indicator_name \
                    RETURNING indicator_uid;".format(indicator.topic.topic_uid, indicator.indicator_name, indicator.indicator_unit))
            self.curr.execute(sql)
            try:
                indicator.indicator_uid = self.curr.fetchone()[0]
                print(indicator.indicator_uid)
                self.conn.commit()
                print(self.curr.rowcount, "indicator records inserted.")
            except:
                print("Indicator %s already existed" % indicator.indicator_name)
            self.conn.commit()
        return

def create_location_uid(self):
    self.curr.execute("SELECT location_uid FROM dim_location ORDER BY location_uid DESC LIMIT 1")
    latest_loc_uid = self.curr.fetchall()

    num = int(re.findall('[0-9]+', str(latest_loc_uid))[0])
    num += 1

    return num

def insert_fact_indicators(self):
        for fact in self.:

