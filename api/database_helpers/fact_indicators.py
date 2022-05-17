import var_indicator
import dim_temporal
import dim_location

class FactIndicator:
    def __init__(self, temporal, location, indicator, data):
        self.temporal = temporal #Temporal object
        self.location = location
        self.indicator = indicator
        self.data = data
