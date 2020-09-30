from copy import deepcopy
import pandas as pd

class CulturalCenter:

    def __init__(self, id, name, passport, content, img_url, events):
        self.id = id
        self.name = name
        self.passport = passport
        self.img_url = img_url
        self.events = events
        self.content = content

    @property
    def row(self):
        row_ = deepcopy(self.passport)
        row_['id'] = self.id
        row_['name'] = self.name
        row_['img_url'] = self.img_url
        row_['content'] = self.content
        return row_

    @property
    def events_pd(self):
        return self.events.data_frame

    @property
    def columns(self):
        return self.row.keys()

    @property
    def columns_event(self):
        return self.events.columns_event

    def __str__(self):
        return str(self.row)


class CulturalCenters:
    def __init__(self, ceneters=[]):
        self.centers = deepcopy(ceneters)

    def add(self, center):
        self.centers.append(center)

    @property
    def columns_cultural_center(self):
        return self.centers[0].columns

    @property
    def columns_event(self):
        return self.centers[0].columns_event

    def save(self, path_pd):
        columns_cultural_centers = self.columns_cultural_center
        columns_events = self.columns_event

        data_cc = pd.DataFrame(columns=columns_cultural_centers)
        data_ev = pd.DataFrame(columns=columns_events)
        for center in self.centers:
            print(f'f cc = {center.id} {center.name}')

            row = center.row
            data_cc = data_cc.append(row, ignore_index=True)
            data_sub_ev = center.events_pd
            data_ev = data_ev.append(data_sub_ev)
        data_cc.to_csv(path_pd + '/cultural_centers.csv', index=False)
        data_ev.to_csv(path_pd + '/events.csv', index=False)
