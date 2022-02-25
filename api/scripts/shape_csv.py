import csv

class ShapeCSV:
    """
    Takes in csv and fits columns and data to the data model.
    """
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.cvs_columns = []
        self.req_data_model_dict = None
        self.setReqDataModelCols()
        # self.compareCSVandDict()

    def csvAsDict(self, csv_file):
        with open(csv_file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    self.cvs_columns.append(f'{", ".join(row)}')
                    line_count += 1
                line_count += 1
            print(f'Processed {line_count} lines.')
            print(f'Column names: {self.cvs_columns}')

    def setReqDataModelCols(self):
        """
        Required data model dictionary.
        """
        self.req_data_model_dict = {"DataSource": {
                                    "DataSource_Name": "", 
                                    "DataSource_Source": ""},
                                "DataSet_Name": "",
                                "DataFile_Name": "",
                                "Temporal_UID": {
                                    "column_name": "", 
                                    "value": ""},
                                "Location": {
                                    "Country_Name": "", 
                                    "Region_Name": "", 
                                    "Division_Name": "",
                                    "State_Name": "",
                                    "County_Name": "", 
                                    "City_Name": "",
                                    "Town_Name": "", 
                                    "Neighborhood_Name": ""},
                                "Categories": "",
                                "Topics": "",
                                "Break_Out": "",
                                "Indicators": {
                                    "Indicator_Name": "",
                                    "Indicator_Unit": ""}
                                }

    def getReqDataModelDict(self):
        return self.req_data_model_dict
    
    def compareCSVandDict(self):
        """
        Gets the columns (substring) of csv (dictionary) and look for similiar columns.
        """
        for cols in self.cvs_columns:
            # Using list comprehension + enumerate()
            # Key index in Dictionary
            temp = list(self.req_data_model_dict.items()) 
            res = (idx for idx, key in enumerate(temp) if key[0] == cols)
            print("Index of search key is : " + str(res))

    def updateReqDict(self, new_dict):
        """
        Adds extra columns found in csv if user wants to keep columns.
        """
        self.req_data_model_dict = new_dict

    def updateDictWithCSV(self):
        """
        Allow user to choose which cols in the csv fits into which key in req dict. 
        For every additional indicator in csv, add to indicators field. 
        Each row, update dim_temperoral and udpate values in fact_indicator. 
        if key was already added, dont add again instead reuse exisitng similiar key.
        """

    def insertShapedDict(self):
        """
        Insert values of updated dictionary to database
        """