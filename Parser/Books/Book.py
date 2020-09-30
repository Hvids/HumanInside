from copy import deepcopy
import pandas as pd


class Book:
    def __init__(self, id, passport, comments):
        self.id = id
        self.passport = passport
        self.comments = comments

    def __str__(self):
        return str(self.row)

    @property
    def row(self):
        res = deepcopy(self.passport)
        res['id'] = self.id
        return res

    @property
    def columns(self):
        return self.row.keys()

    @property
    def columns_comment(self):
        return self.comments.columns

class Books:
    def __init__(self, books=[]):
        self.books = deepcopy(books)

    def add(self, book):
        self.books.append(book)

    @property
    def columns(self):
        return self.books[0].row.keys

    @property
    def columns_comment(self):
        return self.books[0].columns_comment

    def save(self, path_pd):
        df_books = pd.DataFrame(columns=self.columns)
        df_comment = pd.DataFrame(columns=self.columns_comment)

