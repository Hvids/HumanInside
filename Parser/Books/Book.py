from copy import deepcopy
import pandas as pd


class Book:
    def __init__(self, id, passport, comments = None):
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
    def comments_df(self):
        return self.comments.df

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
        return self.books[0].row.keys()

    @property
    def columns_comment(self):
        return self.books[0].columns_comment

    def save(self, path_pd):
        df_books = pd.DataFrame(columns=self.columns)
        # df_comments = pd.DataFrame(columns=self.columns_comment)
        for book in self.books:
            row = book.row
            # df_comments_sub = book.comments_df
            df_books = df_books.append(row,ignore_index=True)
            # df_comments = df_comments.append(df_comments_sub)

        # df_comments.to_csv(path_pd+'/comments.csv', index=False)
        df_books.to_csv(path_pd+'/books.csv',index=False)
