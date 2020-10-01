from copy import deepcopy
import pandas as pd
from tqdm import tqdm


class Data:
    counter = 0
    def __init__(self, passport):
        self.id = self.__class__.counter
        self.__class__.counter += 1
        self.passport = passport

    def __str__(self):
        return str(self.row)

    @property
    def columns(self):
        return self.row.keys()

    @property
    def row(self):
        row = {}
        row['id'] = self.id
        for key, value in self.passport.items():
            row[key] = value
        return row


class DataList:
    name_save = 'data_list'
    def __init__(self, data_list=[]):
        self.data_list = deepcopy(data_list)

    def add(self, data):
        self.data_list.append(data)

    @property
    def size(self):
        return len(self.data_list)

    @property
    def columns(self):
        return self.data_list[0].row

    def save(self, path):
        df = pd.DataFrame(columns=self.columns)
        for data in tqdm(self.data_list, desc=f'Save {self.name}'):
            row = data.row
            df = df.append(row, ignore_index=True)
        df.to_csv(path + self.name_save + '.csv', index=False)

    def __str__(self):
        return str([str(data) for data in self.data_list])
