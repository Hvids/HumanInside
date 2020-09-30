from copy import deepcopy
import pandas as pd


class Event:
    counter = 0

    def __init__(self, id_cultural, name, content, img_url, passport):
        self.id = self.__class__.counter
        self.__class__.counter += 1
        self.name = name
        self.content = content
        self.img_url = img_url
        self.passport = passport
        self.id_cultural = id_cultural

    @property
    def columns(self):
        return self.row.keys()

    @property
    def row(self):
        res = deepcopy(self.passport)
        res['id'] = self.id
        res['id_cultural'] = self.id_cultural
        res['name'] = self.name
        res['img_url'] = self.img_url
        res['content'] = self.content
        return res

    def __str__(self):
        return str(self.row)


class Events:
    def __init__(self, events=[]):
        self.events = events

    @property
    def columns_event(self):
        return self.events[0].columns

    @property
    def data_frame(self):
        columns = self.columns_event
        data_ev = pd.DataFrame(columns=columns)
        for event in self.events:
            row = event.row
            data_ev = data_ev.append(row, ignore_index=True)
        return data_ev

    def add(self, event):
        self.events.append(event)
