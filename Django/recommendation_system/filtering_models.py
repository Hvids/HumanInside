from joblib import load
import pandas as pd
import numpy as np


class Filtering:
    def __init__(self, df, model, k=10):
        self.model = model
        self.k = k
        self.df = df

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

    def predict(self, id_user):
        items = [int(i) for i in self.df.columns if i.isdigit()]
        scores = pd.Series(self.model.predict(id_user, np.arange(len(items))))
        scores_ids = list(pd.Series(scores.sort_values(ascending=False).index))
        know_ids = self.get_know_ids(id_user)
        recommendation_ids = self.get_reccomend(know_ids, scores_ids)[:self.k]
        recommendation_ids = [items[rec] for rec in recommendation_ids]
        return recommendation_ids


class FilteringBooks(Filtering):

    @classmethod
    def load_model(cls, name_data='users_books.csv', path_data='./recommendation_system/data/',
                   name_model='filter_users_books.joblib', path_model='./recommendation_system/models/'):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data)
        return cls(df, model)


class FilteringEvents(Filtering):

    @classmethod
    def load_model(cls, name_data='users_events.csv', path_data='./recommendation_system/data/',
                   name_model='filter_users_events.joblib', path_model='./recommendation_system/models/'):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data)
        return cls(df, model)


class FilteringCulturalCenters(Filtering):

    @classmethod
    def load_model(cls, name_data='users_cultural_centers.csv', path_data='./recommendation_system/data/',
                   name_model='filter_users_cultural_centers.joblib', path_model='./recommendation_system/models/'):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data)
        return cls(df, model)

# from recommendation_system.filtering_models import FilteringBooks,FilteringEvents,FilteringCulturalCenters;
# fb = FilteringBooks.load_model();fb.predict(1)
# fb = FilteringEvents.load_model();fb.predict(1)
# fb = FilteringCulturalCenters.load_model();fb.predict(1)
#
