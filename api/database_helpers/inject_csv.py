#!/usr/bin/python
import re

class InjectCSV():
    def __init__(self, conn, cursor, shape):
        self.conn = conn
        self.curr = cursor
        self.temporals = shape.dim_temporal_objs.temporals
        self.locations = shape.dim_location_objs.locations
        self.categories = shape.var_category_objs.categories
        self.topics = shape.var_topic_objs.topics
        self.indicators = shape.var_indicator_objs.indicators
        self.fact_indicators = shape.fact_indicator_objs.fact_indicators
    def run_injection(self):
        """
        For every object, give it a unique id and inject into HealthBI database.
        """
        self.insert_temporals()
        self.insert_locations()
        self.insert_categories()
        self.insert_topics()
        self.insert_indicators()
        self.insert_fact_indicators()


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
            uid = getattr(self.temporals[0], "temporal_uid")
            year = getattr(self.temporals[0], "year")
            month = getattr(self.temporals[0], "month_99")
            month_name = getattr(self.temporals[0], "month_name")
            day = getattr(self.temporals[0], "day_99")
            sql = ("INSERT INTO dim_temporal VALUES ('{}', '{}', '{}', 'NA', '{}', 'NA', '{}', 'NA', 'NA', 'NA', 'NA', 'NA') \
                        ON CONFLICT(temporal_uid) \
                        DO UPDATE SET temporal_uid=EXCLUDED.temporal_uid \
                        RETURNING temporal_uid".format(uid, year, month, month_name, day))
            self.curr.execute(sql)
            self.conn.commit()
        else:
            for temp in self.temporals:
                uid = getattr(temp, "temporal_uid")
                year = getattr(temp, "year")
                month = getattr(temp, "month_99")
                month_name = getattr(temp, "month_name")
                day = getattr(temp, "day_99")
                sql = ("INSERT INTO dim_temporal VALUES ('{}', '{}', '{}', 'NA', '{}', 'NA', '{}', 'NA', 'NA', 'NA', 'NA', 'NA') \
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
                #print(self.curr.rowcount, "location records inserted.")
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

    def insert_fact_indicators(self):
        print("INSERTING indicators...")
        for fact in self.fact_indicators:
            # return the id of inserted fact_indicator in postgres
            # if topic already existed return its id
            sql = ("INSERT INTO fact_indicator (temporal_uid, location_uid, indicator_uid, indicator_value) \
                    VALUES ({}, {}, {}, {}) \
                    ON CONFLICT (indicator_uid, location_uid, temporal_uid) \
                    DO UPDATE SET indicator_uid=EXCLUDED.indicator_uid, \
                                  location_uid=EXCLUDED.location_uid, \
                                  temporal_uid=EXCLUDED.temporal_uid\
                    RETURNING Fact_UID;".format(20111202, fact.location_object.location_uid, fact.indicator_object.indicator_uid, fact.real_value))
            self.curr.execute(sql)
            try:
                fact.fact_indicator_uid = self.curr.fetchone()[0]
                print(fact.fact_indicator_uid)
                self.conn.commit()
                print(self.curr.rowcount, "fact_indicator records inserted.")
            except:
                print("Fact Indicator %s already existed" % fact.fact_indicator_uid)
            self.conn.commit()
        return