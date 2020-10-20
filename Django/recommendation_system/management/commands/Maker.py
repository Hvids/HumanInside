import pandas as pd
from tqdm import tqdm
from polls.models import Genre, GenreBook
from .PreProcessing import PreProcessingDummies, PreProcessingContent, PreProcessingDropColumns
from lightfm import LightFM
from scipy.sparse import csr_matrix
from joblib import dump
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

import json


class MakerMatrix:
    def save_df(self, df, path, name):
        df.to_csv(path + name, index=False)

    def covert_tuple(self, tuple_list):
        tuple_list = list(tuple_list)
        res = [t[0] for t in tuple_list]
        return res


class MakerMatrixUserTemp(MakerMatrix):
    def __init__(self, User_object, Temp_object, UserTemp_object):
        self.User_object = User_object
        self.Temp_object = Temp_object
        self.UserTemp_object = UserTemp_object

    def get_score(self, id):
        score = self.UserTemp_object.objects.get(id=id).score
        if score == None:
            return 5
        else:
            return score

    def make(self, name_process=''):
        temps_id = self.Temp_object.objects.all().values_list('id')
        temps_id = self.covert_tuple(temps_id)
        users_id = self.User_object.objects.all().values_list('id')
        users_id = self.covert_tuple(users_id)
        res_values = []
        for user_id in tqdm(users_id, desc=name_process):
            select_temps = self.UserTemp_object.objects.filter(id_user=user_id).values_list('id')
            select_temps = self.covert_tuple(select_temps)
            user_values = [self.get_score(id) if id in select_temps else 0 for id in temps_id]
            res_values.append(user_values)
        df = pd.DataFrame(res_values, columns=temps_id)
        df['id'] = users_id

        return df


class MakerMatrixTemp(MakerMatrix):
    def __init__(self, Temp):
        self.Temp = Temp

    def make(self, columns_select):
        temp = self.Temp.objects.all().values_list(*columns_select)
        df = pd.DataFrame(temp, columns=columns_select)
        return df


class MakerMatrixGenre(MakerMatrix):
    def make(self, ids_book):
        genres = Genre.objects.all().values_list('id')
        genres = self.covert_tuple(genres)
        res = []
        for id_book in tqdm(ids_book, desc='MakeGenres'):
            genres_book = GenreBook.objects.filter(book=id_book).values_list('genre')
            res_row = [1 if id_genre in genres_book else 0 for id_genre in genres]
            res.append(res_row)
        df = pd.DataFrame(res, columns=genres)
        return df


class MakerContent:
    @staticmethod
    def get_df_content(content_1, content_2, id):
        df = pd.concat([content_1, content_2], axis=1)
        df['id'] = id
        return df


class MakerMatrixBooks:
    def __init__(self):
        pass

    def make(self, df, load=True):
        maker_matrix_genre = MakerMatrixGenre()
        preprocessing_dummies = PreProcessingDummies()
        preprocessing_content = PreProcessingContent(name='books')

        select_columns = ['id', 'pages', 'rating']

        df_genre = maker_matrix_genre.make(df.id)
        df_author = preprocessing_dummies.make(df.author)
        df_language = preprocessing_dummies.make(df.language)

        df_content_lda = preprocessing_content.make_matrix_lda_with_load(
            df.content) if load else preprocessing_content.make_matrix_lda_with_fit(df.content)
        df_content_w2v = preprocessing_content.make_matrix_w2v(df.content)

        df = df[select_columns]
        df_preprocessing_result_books = pd.concat(
            [df, df_genre, df_content_lda, df_content_w2v, df_author, df_language], axis=1)

        return MakerContent.get_df_content(df_content_lda, df_content_w2v, df.id), df_preprocessing_result_books


class MakerMatrixEvents:
    def make(self, df, load=True):
        select_columns = ['id']
        preprocessing_dummies = PreProcessingDummies()
        preprocessing_content = PreProcessingContent(name='events')

        df_content_lda = preprocessing_content.make_matrix_lda_with_load(
            df.content) if load else preprocessing_content.make_matrix_lda_with_fit(df.content)
        df_content_w2v = preprocessing_content.make_matrix_w2v(df.content)

        df_town = preprocessing_dummies.make(df.town)
        df_age_rate = preprocessing_dummies.make(df.age_rate)
        df = df[select_columns]
        df_preprocessing_result = pd.concat(
            [df, df_town, df_age_rate, df_content_lda, df_content_w2v], axis=1)
        return MakerContent.get_df_content(df_content_lda, df_content_w2v, df.id), df_preprocessing_result


class MakerMatrixCulturalCenters:
    def make(self, df, load=True):
        select_columns = ['id', 'latitude', 'longitude']
        preprocessing_dummies = PreProcessingDummies()
        preprocessing_content = PreProcessingContent(name='cultural_centers')

        df_content_lda = preprocessing_content.make_matrix_lda_with_load(
            df.content) if load else preprocessing_content.make_matrix_lda_with_fit(df.content)
        df_content_w2v = preprocessing_content.make_matrix_w2v(df.content)

        df_udegroud = preprocessing_dummies.make(df.underground)
        df = df[select_columns]
        df_preprocessing_result = pd.concat(
            [df, df_udegroud, df_content_lda, df_content_w2v], axis=1)
        return MakerContent.get_df_content(df_content_lda, df_content_w2v, df.id), df_preprocessing_result


class MakerMatrixLibraries:
    def make(self, df, load=True):
        select_columns = ['id', 'latitude', 'longitude']
        preprocessing_dummies = PreProcessingDummies()
        preprocessing_content = PreProcessingContent(name='libraries')

        df_content_lda = preprocessing_content.make_matrix_lda_with_load(
            df.content) if load else preprocessing_content.make_matrix_lda_with_fit(df.content)
        df_content_w2v = preprocessing_content.make_matrix_w2v(df.content)

        df_region = preprocessing_dummies.make(df.region)
        df = df[select_columns]
        df_preprocessing_result = pd.concat(
            [df, df_region, df_content_lda, df_content_w2v], axis=1)
        return MakerContent.get_df_content(df_content_lda, df_content_w2v, df.id), df_preprocessing_result


class MakerFilteringModels:
    def __init__(self, path_save='./recommendation_system/models/', path_data='./recommendation_system/data/'):
        self.path_data = path_data
        self.path_save = path_save

    def make(self, name):
        df = pd.read_csv(self.path_data + name + '.csv')
        df = df.drop('id', axis=1)
        matrix = csr_matrix(df.values)
        model = LightFM(loss='warp')
        model.fit(matrix)
        dump(model, f'{self.path_save}filter_{name}.joblib')


class MakerSimilarJson:
    def make(self, name, path='./recommendation_system/data/'):
        df = pd.read_csv(f'{path}preprocessing_{name}.csv')
        df_t = df.drop('id', axis=1)
        cosine_similarities = linear_kernel(df_t.values, df_t.values)
        results = {}
        for idx, row in tqdm(df.iterrows(), desc=name):
            similar_indices = cosine_similarities[idx].argsort()[::-1]
            similar_items = [int(df['id'][i]) for i in similar_indices]
            results[int(row['id'])] = similar_items[1:]
        return results

    def save_json(self, data, name, path="./recommendation_system/data/json/"):
        with open(f"{path}{name}.json", "w") as write_file:
            json.dump(data, write_file)
