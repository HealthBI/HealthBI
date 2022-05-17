#!/usr/bin/python
import re

class InjectCSV():
    def __init__(self, conn, cursor, shape):
        self.conn = conn
        self.curr = cursor
        self.temporals = shape.dim_temporal_objs.temporals
        self.datasources = shape.imp_datasource_objs.datasources
        self.datasets = shape.imp_dataset_objs.datasets
        self.datafiles = shape.imp_datafile_objs.datafiles
        self.locations = shape.dim_location_objs.locations
        self.categories = shape.var_category_objs.categories
        self.topics = shape.var_topic_objs.topics
        self.indicators = shape.var_indicator_objs.indicators

    def run_injection(self):
        """
        For every object, give it a unique id and inject into HealthBI database.
        """
        self.insert_temporals()
        self.insert_location()
        self.insert_datasources()
        self.insert_datasets()
        self.insert_datafiles()
        self.insert_categories()
        self.insert_topics()
        self.insert_indicator()

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
                        RETURNING temporal_uid".format(uid, year, month, month_name, day))
                self.curr.execute(sql)
                self.conn.commit()
        return

    def insert_location(self):

        for obj in self.locations:
            if hasattr(obj, 'location_uid'):
                break
            else:
                loc_uid = self.create_location_uid()
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
    
    def insert_datasources(self):
        print("Inserting datasources...")

        for datasource in self.datasources:

            sql = ("INSERT INTO IMP_DATASOURCE (DataSource_Name, DataSource_Source) VALUES ('{}', '{}') \
                    ON CONFLICT(DataSource_Name, DataSource_Source) \
                    DO UPDATE SET DataSource_Name = EXCLUDED.DataSource_Name \
                    RETURNING DataSource_UID".format(datasource.DataSource_Name, datasource.DataSource_Source))
            self.curr.execute(sql)

            try:
                datasource.DataSource_UID = self.curr.fetchtone()[0]
                print(datasource.DataSource_UID)
                self.conn.commit()
                print(self.curr.rowcount, "datasource records inserted.")
            except:
                print("Datasource %s already exists" %datasource.DataSource_Name)
            
            self.conn.commit()
        
        return
    
    def insert_datasets(self):
        print("Inserting datasets...")

        for dataset in self.datasets:

            sql = ("INSERT INTO IMP_DATASET (DataSet_Name, DataSource_UID) VALUES('{}', '{}') \
                    ON CONFLICT(DataSet_Name, DataSource_UID) \
                    DO UPDATE SET DataSet_Name = EXCLUDED.DataSet_Name \
                    RETURNING DataSet_UID".format(dataset.DataSet_Name, dataset.datsource.DataSource_UID))
            self.curr.execute(sql)

            try:
                dataset.DataSet_UID = self.curr.fetchtone()[0]
                print(dataset.DataSet_UID)
                self.conn.commit()
                print(self.curr.rowcount, "dataset records inserted.")
            except:
                print("Dataset %s already exists" %dataset.DataSet_Name)
            
            self.conn.commit()
        
        return

    def insert_datafiles(self):
        print("Inserting datafiles...")

        for datafile in self.datafiles:

            sql = ("INSERT INTO IMP_DATAFILE (DataFile_Name, Import_Timestamp, DataSet_UID) VALUES ('{}', '{}', '{}') \
                    ON CONFLICT(DataFile_Name, Import_Timestamp, DataSet_UID) \
                    DO UPDATE SET DataFile_Name = EXCLUDED.DataFile_Name \
                    RETURNING Import_UID".format(datafile.DataFile_Name, datafile.Import_Timestamp, datafile.dataset.DataSet_UID))

            self.curr.execute()

            try:
                datafile.Import_UID = self.curr.fetchtone()[0]
                print(datafile.Import_UID)
                self.conn.commit()
                print(self.curr.rowcount, "datafile records inserted.")
            except:
                print("Datafile %s already exists" %datafile.DataFile_Name)

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



