import pandas as pd
from PIL import Image
import requests
from io import BytesIO

from copy import deepcopy


class Library:
    def __init__(self, name, passport, img_url, content):
        self.name = name
        self.passport = passport
        self.img_url = img_url
        self.content = content
        self.row = self.__make_row()
        self.id_column_name = 'id_library'

    def __make_row(self):
        row = {}
        row['name'] = self.name
        for key in self.passport.keys():
            row[key] = self.passport[key]
        row['img_url'] = self.img_url
        row['content'] = self.content
        return row

    def save_img(self, id, path_img):
        response = requests.get(self.img_url)
        img = Image.open(BytesIO(response.content))
        img.convert('RGB').save(path_img + str(id)+'.png', "PNG", optimize=True)

    def get_row_for_pandas(self, id):
        row = deepcopy(self.row)
        row[self.id_column_name] = id
        return row

    @property
    def attrs_name(self):
        attrs = [self.id_column_name] + list(self.row.keys())
        return attrs

    def __str__(self):
        return str(self.row)
