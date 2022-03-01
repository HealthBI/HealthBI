import csv
from dim_temporal import Temporal
'''
temporals = []
locations = []
indicators = []
facts = []
row by row
    temp = temporals.append(temporal)
    loc = locations.append(location)
    indi = indicators.append(indicator)
    fact = facts.append(fact_ind(temp, loc, indi, val))
done reading csv
inject(temporals) -> update each temp.uid
inject(locations) -> update each loc.uid
inject(indicators) -> update each indi.uid
inject(fact) -> 
'''
class HealthBIData:
    def __init__(self):
        self.Temporals = []
        self.Locations = []
        self.Indicators = []
        self.Facts = []

    def createNewTemporal(self, temporal):
        for temp_index in range(len(self.Temporals)):
            if temporal == self.Temporals[temp_index]:
                return self.Temporals[temp_index]
            else:
                #TODO: Make sure the right object is returned
                # so that the right uid is updated in the fact object
                self.Temporals.append(temporal)
                return self.Temporals[-1]

    def readCSV(self, filename):
        # read row by row
        '''    
        temp = temporals.append(temporal)
        loc = locations.append(location)
        indi = indicators.append(indicator)
        fact = facts.append(fact_ind(temp, loc, indi, val))
        '''
        temporal = get_csv_row(temporal_column_name)
        temp = createNewTemporal(Temporal(temporal))
        pass
