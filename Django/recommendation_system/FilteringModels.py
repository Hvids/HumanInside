from joblib import load
import numpy as np
from .Maker import *
from .names import *
from .paths import *
from polls.models import *


class Filtering:
    def __init__(self, df,  model,LastObject, name_object, k=10):
        self.LastObject = LastObject
        self.name_object = name_object
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
        ids = self.LastObject.objects.filter(id_user=user_id).values_list(self.name_object)
        ids = [i[0] for i in ids]
        return ids

    def get_reccomend(self, knows, rec_ids):
        return [int(rec) for rec in rec_ids if int(rec) not in knows]

    def recommend(self, id_user):
        index_user = self.user_index_dict[id_user]
        scores = pd.Series(self.model.predict(index_user, np.arange(len(self.index_item_dict.keys()))))
        scores_ids = list(pd.Series(scores.sort_values(ascending=False).index))
        know_ids = self.get_know_ids(id_user)

        recommendation_ids = [self.index_item_dict[rec] for rec in scores_ids]
        # print(know_ids)
        recommendation_ids = self.get_reccomend(know_ids, recommendation_ids)
        # print(recommendation_ids)
        return recommendation_ids[:self.k]

    def update(self, maker_filtering_matrix, maker_filtering_model):
        maker_filtering_matrix.make()
        maker_filtering_model.make()


class FilteringBooks(Filtering):
    @classmethod
    def load_model(cls, name_data=FILTER_MATRIX_USERS_BOOKS, path_data=PATH_DATA_CSV,
                   name_model=FILTERING_MODEL_BOOKS, path_model=PATH_MODELS, k=5):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data + '.csv')
        return cls(df, model, LastObject=LastBook, name_object='id_book', k=k)

    def update(self):
        maker_filter_matrix = MakerFilteringMatrixBooks()
        maker_filter_model = MakerFilteringModelBooks()
        super(FilteringBooks, self).update(maker_filter_matrix, maker_filter_model)
        return FilteringBooks.load_model()


class FilteringEvents(Filtering):

    @classmethod
    def load_model(cls, name_data=FILTER_MATRIX_USERS_EVENTS, path_data=PATH_DATA_CSV,
                   name_model=FILTERING_MODEL_EVENTS, path_model=PATH_MODELS, k=5):
        model = cls.load(name_model, path_model)
        df = pd.read_csv(path_data + name_data + '.csv')
        return cls(df, model, LastObject=LastEvent, name_object='id_event', k=k)

    def update(self):
        maker_filter_matrix = MakerFilteringMatrixEvents()
        maker_filter_model = MakerFilteringModelEvents()
        super(FilteringEvents, self).update(maker_filter_matrix, maker_filter_model)
        return FilteringBooks.load_model()
