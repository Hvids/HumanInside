from joblib import load
import numpy as np
from .Maker import *
from polls.models import *
from .names import *
from .paths import *


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
        model = load(path + name + '.joblib')
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

    def update(self, maker_filtering_matrix, maker_filtering_model):
        maker_filtering_matrix.make()
        maker_filtering_model.make()


class FilteringBooks(Filtering):
    @classmethod
    def load_model(cls, name_data=FILTER_MATRIX_USERS_BOOKS, path_data=PATH_DATA_CSV,
                   name_model=FILTERING_MODEL_BOOKS, path_model=PATH_MODELS):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data + '.csv')
        return cls(df, model)

    def update(self):
        maker_filter_matrix = MakerFilteringMatrixBooks()
        maker_filter_model = MakerFilteringModelBooks()
        super(FilteringBooks, self).update(maker_filter_matrix, maker_filter_model)
        return FilteringBooks.load_model()


class FilteringEvents(Filtering):

    @classmethod
    def load_model(cls, name_data=FILTER_MATRIX_USERS_EVENTS, path_data=PATH_DATA_CSV,
                   name_model=FILTERING_MODEL_EVENTS, path_model=PATH_MODELS):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data + '.csv')
        return cls(df, model)

    def update(self):
        maker_filter_matrix = MakerFilteringMatrixEvents()
        maker_filter_model = MakerFilteringModelEvents()
        super(FilteringEvents, self).update(maker_filter_matrix, maker_filter_model)
        return FilteringBooks.load_model()


class FilteringCulturalCenters(Filtering):

    @classmethod
    def load_model(cls, name_data=FILTER_MATRIX_USERS_CULTURAL_CENTERS, path_data=PATH_DATA_CSV,
                   name_model=FILTERING_MODEL_CULTURAL_CENTERS, path_model=PATH_MODELS):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data + '.csv')
        return cls(df, model)

    def update(self):
        maker_filter_matrix = MakerFilteringMatrixCulturalCenters()
        maker_filter_model = MakerFilteringModelCulturalCenters()
        super(FilteringCulturalCenters, self).update(maker_filter_matrix, maker_filter_model)
        return FilteringBooks.load_model()
