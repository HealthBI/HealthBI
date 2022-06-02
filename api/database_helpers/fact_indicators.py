class Fact:
    def __init__(self, location_object, indicator_object, real_value):
        self.fact_indicator_uid = None
        self.temporal_uid = None #Temporal object
        self.location_object = location_object
        self.indicator_object = indicator_object
        self.real_value = real_value
class FactIndicator():
    def __init__(self):
        self.fact_indicators = []
        self.num_fact_indicators = 0
    def create_new_fact_indicator(self, row, location_object, indicator_object):
        fact = Fact(location_object, indicator_object, row[indicator_object.indicator_name])
        self.fact_indicators.append(fact)

        self.num_fact_indicators += 1
        return fact
