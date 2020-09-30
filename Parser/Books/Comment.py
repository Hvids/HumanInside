from copy import deepcopy
import pandas as pd

class Comment:
    counter = 0

    def __init__(self, id_book, date, rating, content):
        self.id = self.__class__.counter
        self.__class__.counter += 1
        self.id_book = id_book
        self.date = date
        self.rating = rating
        self.content = content

    def __str__(self):
        return str(self.row)

    @property
    def row(self):
        res = {
            'id': self.id,
            'id_book': self.id_book,
            'date': self.date,
            'rating': self.rating,
            'content': self.content
        }
        return res

    @property
    def columns(self):
        return ['id', 'id_book', 'date', 'rating', 'content']


class Comments:
    def __init__(self, comments=[]):
        self.comments = deepcopy(comments)

    def add(self,value):
        self.comments.append(value)
    @property
    def columns(self):
        return ['id', 'id_book', 'date', 'rating', 'content']

    @property
    def df(self):
        df =pd.DataFrame(columns=self.columns)
        for com in self.comments:
            row = com.row
            df = df.append(row,ignore_index=True)
        return df
