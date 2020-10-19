from .Updater import *
from joblib import load
import pandas as pd
import numpy as np
from .management.commands.Maker import MakerMatrixUserTemp, MakerFilteringModels
from polls.models import *
from .Updater import UpdateFilterModel


class Filtering:
    def __init__(self, df, model, k=10):
        self.model = model
        self.k = k
        self.df = df
        self.index_item_dict = self.get_index_item_dict(df.drop('id', axis=1).columns)
        self.index_user_dict = self.get_index_user_dict(df.id)
        self.user_index_dict = self.get_user_index_dict((df.id))

    def get_index_item_dict(self, columns):
        return {index: columns[index] for index in range(len(columns))}

    def get_user_index_dict(self, ids):
        return {ids[index]: index for index in range(len(ids))}

    def get_index_user_dict(self, ids):
        return {index: ids[index] for index in range(len(ids))}

    @staticmethod
    def load(name, path):
        model = load(path + name)
        return model

    def get_know_ids(self, user_id):
        user = self.df[self.df.id == user_id]
        user = user.drop('id', axis=1)
        user = user.iloc[0]
        return list(user[user != 0])

    def get_reccomend(self, knows, scores_ids):
        return [score for score in scores_ids if score not in knows]

    def recommend(self, id_user):
        index_user = self.user_index_dict[id_user]
        scores = pd.Series(self.model.predict(index_user, np.arange(len(self.index_item_dict.keys()))))
        scores_ids = list(pd.Series(scores.sort_values(ascending=False).index))
        know_ids = self.get_know_ids(id_user)
        recommendation_ids = self.get_reccomend(know_ids, scores_ids)[:self.k]
        recommendation_ids = [self.index_item_dict[rec] for rec in recommendation_ids]
        return recommendation_ids

    def update_with_updater(self, updater):
        updater.update()


class FilteringBooks(Filtering):
    @classmethod
    def load_model(cls, name_data='users_books.csv', path_data='./recommendation_system/data/',
                   name_model='filter_users_books.joblib', path_model='./recommendation_system/models/'):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data)
        return cls(df, model)

    def update(self):
        updater = UpdateFilterModel(
            name_matrix='users_books.csv',
            path_matrix='./recommendation_system/data/',
            name_model='filter_users_books.joblib',
            path_model='./recommendation_system/models/',
            maker_matrix=MakerMatrixUserTemp(User, Book, LastBook),
            name_for_maker_model='users_books',
            maker_model=MakerFilteringModels()
        )
        self.update_with_updater(updater)
        return FilteringBooks.load_model()


class FilteringEvents(Filtering):

    @classmethod
    def load_model(cls, name_data='users_events.csv', path_data='./recommendation_system/data/',
                   name_model='filter_users_events.joblib', path_model='./recommendation_system/models/'):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data)
        return cls(df, model)

    def update(self):
        updater = UpdateFilterModel(
            name_matrix='users_events.csv',
            path_matrix='./recommendation_system/data/',
            name_model='filter_users_events.joblib',
            path_model='./recommendation_system/models/',
            maker_matrix=MakerMatrixUserTemp(User, Event, LastEvent),
            name_for_maker_model='users_events',
            maker_model=MakerFilteringModels()
        )
        self.update_with_updater(updater)
        return FilteringEvents.load_model()


class FilteringCulturalCenters(Filtering):

    @classmethod
    def load_model(cls, name_data='users_cultural_centers.csv', path_data='./recommendation_system/data/',
                   name_model='filter_users_cultural_centers.joblib', path_model='./recommendation_system/models/'):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data)
        return cls(df, model)

    def update(self):
        updater = UpdateFilterModel(
            name_matrix='users_cultural_centers.csv',
            path_matrix='./recommendation_system/data/',
            name_model='filter_users_cultural_centers.joblib',
            path_model='./recommendation_system/models/',
            maker_matrix=MakerMatrixUserTemp(User, CultureCenter, UserTemp),
            name_for_maker_model='users_cultural_centers',
            maker_model=MakerFilteringModels()
        )
        self.update_with_updater(updater)
        return FilteringCulturalCenters.load_model()
