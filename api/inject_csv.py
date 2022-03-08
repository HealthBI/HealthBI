#!/usr/bin/python
from ast import Return
import re

from matplotlib.pyplot import get

#from scripts.dim_location import DimLocation
#from scripts.dim_temporal import DimTemporal
#from scripts.var_indicator import Indicators

class InjectCSV():
    def __init__(self, conn, cursor, shape):
        self.conn = conn
        self.curr = cursor
        #self.dim_temporal_objs = shape.dim_temporal_objs
        self.categories = shape.var_category_objs.categories
        self.topics = shape.var_topic_objs.topics
        self.indicators = shape.var_indicator_objs.indicators
    def run_injection(self):
        """
        For every object, give it a unique id and inject into HealthBI database.
        """
        #self.insert_temporal()
        self.insert_categories()
        self.insert_topics()
        self.insert_indicator()

    def insert_temporal(self):
        """
        Give every temporal object a temporal_uid then insert.
        """
        for obj in self.dim_temporal_objs:
            # Give the object a temporal_uid
            if hasattr(obj,'temporal_uid'):
                break
            else:
                tem_uid = self.create_temporal_uid()
                setattr(obj,'temporal_uid', tem_uid) 
            # Insert the object. NOTE: This only injects year. Get json column name
            tem_uid = getattr(obj, 'temporal_uid')
            tem_value = getattr(obj, 'value')
            print(int(tem_uid))
            print(tem_value)
            # TODO: Insert if json val col does not exist in database. Check the uid after editing incrementation, select count is the best way to check for uniqueness
            sql = ("INSERT INTO dim_temporal VALUES ('{}', '{}', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA') WHERE ON CONFLICT DO NOTHING;".format(tem_uid, tem_value))
            self.curr.execute(sql)
            self.conn.commit()
            print(self.curr.rowcount, "records inserted.")

    def create_temporal_uid(self):
        """
        Creates temporal_uid. Mask to correct number of digits, year, month, and day (bigint)
        """
        # TODO: for devang, temporal_uid has to be format yearmonthday (12341212)
        self.curr.execute("SELECT temporal_uid FROM dim_temporal ORDER BY temporal_uid DESC LIMIT 1")
        latest_tem_uid = self.curr.fetchall()
        print(latest_tem_uid)
        num = int(re.findall('[0-9]+', str(latest_tem_uid))[0])
        num += 1
        return num

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
                print(self.curr.rowcount, "topic records inserted.")
            except:
                print("Topic %s already existed" % topic.topic_name)
            self.conn.commit()
        return

    def insert_indicator(self):
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
