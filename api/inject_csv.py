#!/usr/bin/python
import re

from matplotlib.pyplot import get

from api.scripts.dim_location import DimLocation
from api.scripts.dim_temporal import DimTemporal

class InjectCSV():
    def __init__(self, conn, cursor, dim_temporal_objs):
        self.conn = conn
        self.curr = cursor
        self.dim_temporal_objs = dim_temporal_objs

    def run_injection(self):
        """
        For every object, give it a unique id and inject into HealthBI database.
        """
        self.insert_temporal()

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


        