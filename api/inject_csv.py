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
<<<<<<< Updated upstream
        self.dim_temporal_objs = shape.dim_temporal_objs
=======
        #self.dim_temporal_objs = shape.dim_temporal_objs
        self.temporals = shape.dim_temporal_objs.temporals
>>>>>>> Stashed changes
        self.categories = shape.var_category_objs.categories
        self.topics = shape.var_topic_objs.topics
        self.indicators = shape.var_indicator_objs.indicators
        self.dim_location_objs = shape.dim_location_objs
    def run_injection(self):
        """
        For every object, give it a unique id and inject into HealthBI database.
        """
        #self.insert_temporal()
        self.insert_temporals()
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
            print(tem_uid)
            print(tem_value)

            self.curr.execute("SELECT Year FROM dim_temporal ORDER BY Year")
            value = self.curr.fetchall()
            # TODO: Insert if json val col does not exist in database. Check the uid after editing incrementation, select count is the best way to check for uniqueness

            # sql = ("INSERT INTO dim_temporal VALUES ('{}', '{}', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA');".format(tem_uid, tem_value))
            # self.curr.execute(sql)
            # self.conn.commit()
            # print(self.curr.rowcount, "records inserted.")
            self.curr.execute("SELECT COUNT(*) FROM dim_temporal WHERE Year = %s", [tem_value])
            check = self.curr.fetchall()
            print(check, "check json val")
            count = int(re.findall('[0-9]+', str(check))[0])
            if(count == 0):
                sql = ("INSERT INTO dim_temporal VALUES ('{}', '{}', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA');".format(tem_uid, tem_value))
                self.curr.execute(sql)
                self.conn.commit()
                print(self.curr.rowcount, "records inserted.")
            else:
                print("Year value already exists in the table")
            

    def create_temporal_uid(self):
        """
        Creates temporal_uid. Mask to correct number of digits, year, month, and day (bigint)
        """
        # TODO: for devang, temporal_uid has to be format yearmonthday (12341212)
        self.curr.execute("SELECT temporal_uid FROM dim_temporal ORDER BY temporal_uid DESC LIMIT 1")
        latest_tem_uid = self.curr.fetchall()

        print(latest_tem_uid, "temporal_uid")
        print(str(latest_tem_uid), "temporal_uid string\n")

        # latest_tem_uid = np.array(latest_tem_uid)
        # print(len(latest_tem_uid[0]), "temporal_uid length")
        # print(latest_tem_uid, "temporal_uid np array")
        # print(latest_tem_uid[0], "temporal_uid list")
        # print(latest_tem_uid[0][0], "temporal_uid element")
        # print(type(latest_tem_uid[0][0]), "temporal_uid element type\n")

        month = "00"
        day = "00"
        # latest_tem_uid = str(latest_tem_uid[0][0]) + month + day
        num = int(re.findall('[0-9]+', str(latest_tem_uid))[0])
        num = str(num)
        num = num.rstrip("0")
        print(num, "before increment")
        num = int(num)
        num += 1
        print(num, "after increment")
        num = int(str(num) + month + day)
        print(num, "formatting\n")
        return num

    def insert_temporals(self):
        print("INSERTING temporals...")
        for temp in self.temporals:
            sql = ("INSERT INTO dim_temporal VALUES ('{}', '{}', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA') \
                    ON CONFLICT(temporal_uid) \
                    DO UPDATE SET temporal_uid=EXCLUDED.temporal_uid \
                    RETURNING temporal_uid".format(temp.temporal_uid, temp.year))

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


def insert_location(self):

    for obj in self.dim_location_objs:
        if hasattr(obj, 'location_uid'):
            break
        else:
            loc_uid = create_location_uid()
            setattr(obj, 'location_uid', loc_uid)
        
        loc_uid = getattr(obj, 'location_uid')

        print(loc_uid, "location_uid")

        sql = ("INSERT INTO DIM_LOCATION VALUES({}, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA');".format(loc_uid))
        self.curr.execute(sql)
        self.conn.commit()
        print(self.curr.rowcount, "records inserted.")

def create_location_uid(self):
    self.curr.execute("SELECT location_uid FROM dim_location ORDER BY location_uid DESC LIMIT 1")
    latest_loc_uid = self.curr.fetchall()

    num = int(re.findall('[0-9]+', str(latest_loc_uid))[0])
    num += 1

    return num

