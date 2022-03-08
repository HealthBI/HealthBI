import json
from unicodedata import category
from pandas import *

class Category:
    def __init__(self, category_name):
        self.category_uid = None #created after insertion to POSTGRES
        self.category_name = category_name
    def __eq__(self, other):
        return self.category_name == other.category_name
class Categories:
    def __init__(self):
        self.categories = []
        self.num_of_categories = 0
    def add(self, category):
        # returning the category in list of categories
        if self.num_of_categories == 0:
            self.categories.append(category)
            self.num_of_categories += 1
            print("A new category has been created: {}.".format(category.category_name))
            return self.categories[-1]
        else:
            for i in range(self.num_of_categories):
                if category == self.categories[i]:
                    print("This category has already been created.")
                    return self.categories[i]
                else: 
                    self.categories.append(category)
                    self.num_of_categories += 1
                    print("A new category has been created: {}.".format(category.category_name))
                    return self.categories[-1]
    
class Topic():
    def __init__(self, category, topic_name):
        self.category = category
        self.topic_uid = None #created after insertion to POSTGRES
        self.topic_name = topic_name
    def __eq__(self, other):
        return self.category == other.category and self.topic_name == other.topic_name

class Topics:
    def __init__(self):
        self.topics = []
        self.num_of_topics = 0
    def add(self, topic):
        if self.num_of_topics == 0:
            self.topics.append(topic)
            self.num_of_topics += 1
            print("A new topic has been created: {}.".format(topic.topic_name))
            return self.topics[-1]
        else:
            # returning the category in list of categories
            for i in range(self.num_of_topics):
                if category == self.topics[i]:
                    print("This topic has already been created: {}.".format(topic.topic_name))
                    return self.topics[i]
                else: 
                    self.topics.append(topic)
                    self.num_of_topics += 1
                    print("A new topic has been created: {}.".format(topic.topic_name))
                    return self.topics[-1]

class Indicator():
    def __init__(self, topic, indicator_name, indicator_unit):
        self.topic = topic
        self.indicator_uid = None #created after insertion to POSTGRES
        self.indicator_name = indicator_name
        self.indicator_unit = indicator_unit

    def __eq__(self, other):
            if self.topic ==other.topic and self.indicator_name==other.indicator_name:
                return True
            else:
                return False

class Indicators:
    def __init__(self):
        self.indicators = []
        self.num_of_indicators = 0
    def add(self, indicator):
        if self.num_of_indicators == 0:
            self.indicators.append(indicator)
            self.num_of_indicators += 1
            print("A new indicator has been created: {}.".format(indicator.indicator_name))
            return self.indicators[-1]
        else:
            # returning the Indicator in list of indicators
            for i in range(self.num_of_indicators):
                if indicator == self.indicators[i]:
                    print("This indicator has already been created.")
                    return self.indicators[i]
                else: 
                    self.indicators.append(indicator)
                    self.num_of_indicators += 1
                    print("A new indicator has been created: {}.".format(indicator.indicator_name))
                    return self.indicators[-1]

class IndicatorController:
    def __init__(self) -> None:
        pass
    def create_var_indicator_with_mapping(self, mapping):
        categories = Categories()
        topics = Topics()
        indicators = Indicators()
        for c in range(len(mapping["Categories"])):
            category_name = mapping["Categories"][c]["Category"]
            category = categories.add(Category(category_name))
            for t in range(len(mapping["Categories"][c]["Topics"])):
                topic_name = mapping["Categories"][c]["Topics"][t]["Topic"]
                topic = topics.add(Topic(category, topic_name))
                for i in range(len(mapping["Categories"][c]["Topics"][t]["Indicators"])):
                    indicator_name = mapping["Categories"][c]["Topics"][t]["Indicators"][i]["Indicator_Name"]
                    indicator_unit = mapping["Categories"][c]["Topics"][t]["Indicators"][i]["Indicator_Unit"]
                    indicators.add(Indicator(topic, indicator_name, indicator_unit))
        return categories, topics, indicators