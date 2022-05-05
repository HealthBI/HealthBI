import var_indicator
import dim_temporal
import dim_location
import imp_datafile

class FactIndicator:
    def __init__(self, temporal, location, indicator, data):
        self.temporal = temporal #Temporal object
        self.location = location
        self.indicator = indicator
        self.data = data
