from copy import deepcopy
import pandas as pd
from PIL import Image
import requests
from io import BytesIO


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

    def save_img_events(self, path):
        self.events.save_imgs(path)

    @property
    def events_pd(self):
        return self.events.data_frame

    @property
    def columns(self):
        return self.row.keys()

    @property
    def columns_event(self):
        return self.events.columns_event

    def save_img(self, path_img):
        try:
            id = self.id
            response = requests.get(self.img_url)
            img = Image.open(BytesIO(response.content))
            img.convert('RGB').save(path_img + str(id)+'.png', "PNG", optimize=True)
        except OSError:
            print(f'non image download {self.id}')

    def __str__(self):
        return str(self.row)


class CulturalCenters:
    def __init__(self, ceneters=[]):
        self.centers = ceneters

    def add(self, center):
        self.centers.append(center)

    @property
    def columns_cultural_center(self):
        return self.centers[0].columns

    @property
    def columns_event(self):
        return self.centers[0].columns_event

    def save(self, path_pd, path_img_cultural_center, path_img_event):
        columns_cultural_centers = self.columns_cultural_center
        columns_events = self.columns_event

        data_cc = pd.DataFrame(columns=columns_cultural_centers)
        data_ev = pd.DataFrame(columns=columns_events)
        for center in self.centers:
            center.save_img(path_img_cultural_center)
            center.save_img_events(path_img_event)
            row = center.row
            data_cc = data_cc.append(row, ignore_index=True)
            data_sub_ev = center.events_pd
            data_ev = pd.concat([data_ev, data_sub_ev], axis=1)
        data_cc.to_csv(path_pd + '/cultural_centers.csv', index=False)
        data_ev.to_csv(path_pd + '/events.csv', index=False)
