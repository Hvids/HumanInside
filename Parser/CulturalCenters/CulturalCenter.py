import sys

sys.path.extend(['../'])
from Data import DataList, Data


class CulturalCenter(Data):
    name = 'Cultural Center'
    def __init__(self, passport, events):
        super().__init__(passport)
        self.events = events


class CulturalCenters(DataList):
    name = 'CulturalCenters'
    name_save = 'cultural_center'

    def save(self, path_pd):
        super().save(path_pd)
        self.data_list[0].events.save(path_pd)