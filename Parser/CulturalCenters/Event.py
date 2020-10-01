import sys

sys.path.extend(['../'])
from Data import DataList, Data

class Event(Data):
    name = 'Event'
    def __init__(self, id_cultural, passport):
        super().__init__(passport)
        self.passport['id_cultural'] = id_cultural

class Events(DataList):
    name = 'Events'
    name_save = 'events'
    def __init__(self, data_list=[]):
        self.data_list = data_list


