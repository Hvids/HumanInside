import pandas as pd
from tqdm import tqdm
from polls.models import *
from .names import *
from .paths import *

from .PreProcessing import PreProcessingDummies, PreProcessingContent

from lightfm import LightFM
from scipy.sparse import csr_matrix
from joblib import dump
import json
from sklearn.metrics.pairwise import linear_kernel


class MakerMatrix:
    def save_df(self, df, path, name):
        df.to_csv(path + name + '.csv', index=False)

    def covert_tuple(self, tuple_list):
        tuple_list = list(tuple_list)
        res = [t[0] for t in tuple_list]
        return res


class MakerFilteringMatrixBase(MakerMatrix):
    def __init__(self, ObjectWhoSelect, ObjectWhatSelect, WhoWhatObjectSelect, name_matrix='base',
                 path_csv=PATH_DATA_CSV):
        self.ObjectWhoSelect = ObjectWhoSelect
        self.ObjectWhatSelect = ObjectWhatSelect
        self.WhoWhatObjectSelect = WhoWhatObjectSelect
        self.path_csv = path_csv
        self.name_matrix = name_matrix

    def get_score(self, id):
        score = self.WhoWhatObjectSelect.objects.get(id=id).score
        if score == None:
            return 5
        else:
            return score

    def make(self, save=True):
        id_items = self.ObjectWhatSelect.objects.all().values_list('id')
        id_items = self.covert_tuple(id_items)
        id_users = self.ObjectWhoSelect.objects.all().values_list('id')
        id_users = self.covert_tuple(id_users)
        res_values = []
        for user_id in tqdm(id_users, desc=self.name_matrix):
            select_temps = self.WhoWhatObjectSelect.objects.filter(id_user=user_id).values_list('id')
            select_temps = self.covert_tuple(select_temps)
            user_values = [self.get_score(id) if id in select_temps else 0 for id in id_items]
            res_values.append(user_values)
        df = pd.DataFrame(res_values, columns=id_items)
        df['id'] = id_users

        if save:
            self.save_df(df, self.path_csv, self.name_matrix)

        return df


class MakerFilteringMatrixBooks(MakerFilteringMatrixBase):
    def __init__(
            self,
            ObjectWhoSelect=User,
            ObjectWhatSelect=Book,
            WhoWhatObjectSelect=LastBook,
            name_matrix=FILTER_MATRIX_USERS_BOOKS
    ):
        super(MakerFilteringMatrixBooks, self).__init__(ObjectWhoSelect, ObjectWhatSelect, WhoWhatObjectSelect,
                                                        name_matrix)


class MakerFilteringMatrixEvents(MakerFilteringMatrixBase):
    def __init__(
            self,
            ObjectWhoSelect=User,
            ObjectWhatSelect=Event,
            WhoWhatObjectSelect=LastEvent,
            name_matrix=FILTER_MATRIX_USERS_EVENTS
    ):
        super(MakerFilteringMatrixEvents, self).__init__(ObjectWhoSelect, ObjectWhatSelect, WhoWhatObjectSelect,
                                                         name_matrix)


class MakerFilteringMatrixCulturalCenters(MakerFilteringMatrixBase):
    def __init__(
            self,
            ObjectWhoSelect=User,
            ObjectWhatSelect=CultureCenter,
            WhoWhatObjectSelect=LastCenter,
            name_matrix=FILTER_MATRIX_USERS_CULTURAL_CENTERS
    ):
        super(MakerFilteringMatrixCulturalCenters, self).__init__(ObjectWhoSelect, ObjectWhatSelect,
                                                                  WhoWhatObjectSelect,
                                                                  name_matrix)


class MakerMatrixForPreprocessing:
    def __init__(self, Objcet):
        self.Object = Objcet

    def make(self, columns_select):
        temp = self.Object.objects.all().values_list(*columns_select)
        df = pd.DataFrame(temp, columns=columns_select)
        return df


class MakerMatrixGenre(MakerMatrix):
    def __init__(self, Object=Genre, ObjectSelect=GenreBook, name=GENRES):
        self.Object = Object
        self.ObjectSelect = ObjectSelect
        self.name = name

    def make(self, ids_book):
        genres = self.Object.objects.all().values_list('id')
        genres = self.covert_tuple(genres)
        res = []
        for id_book in tqdm(ids_book, desc=self.name):
            genres_book = self.ObjectSelect.objects.filter(book=id_book).values_list('genre')
            res_row = [1 if id_genre in genres_book else 0 for id_genre in genres]
            res.append(res_row)
        df = pd.DataFrame(res, columns=genres)
        return df


class MakerMatrixBase:
    def __init__(self, name_matrix, columns_dummies, columns_select, name_lda, name_count_vectorizer,
                 content_name='content'):
        self.columns_dummies = columns_dummies
        self.columns_select = columns_select
        self.name_matrix = name_matrix
        self.preprocessing_content = PreProcessingContent(self.name_matrix, name_lda, name_count_vectorizer)
        self.preprocessing_dummies = PreProcessingDummies()
        self.content_name = content_name

    def make_content(self, df, fit):
        content = df[self.content_name]
        df_content_lda = self.preprocessing_content.make_matrix_lda_with_load(
            content) if not fit else self.preprocessing_content.make_matrix_lda_with_fit(content)

        df_content_w2v = self.preprocessing_content.make_matrix_w2v(content)
        return pd.concat([df_content_w2v, df_content_lda], axis=1)

    def make_dummies(self, df):
        dummies_dfs = []
        for column_name in self.columns_dummies:
            column = df[column_name]
            df_sub = self.preprocessing_dummies.make(column)
            dummies_dfs.append(df_sub)
        return pd.concat(dummies_dfs, axis=1)

    def make_select(self, df):
        return df[self.columns_select]

    def make(self, df, fit=True):
        df_content = self.make_content(df, fit)
        df_dummies = self.make_dummies(df)
        df_select = self.make_select(df)
        df_concat = pd.concat([df_select, df_dummies, df_content], axis=1)
        df_content['id'] = df_concat.id
        return df_content, df_concat


class MakerMatrixBooks(MakerMatrixBase):
    def __init__(
            self,
            name_matrix=BOOKS,
            columns_dummies=['author', 'language'],
            columns_select=['id', 'pages', 'rating'],
            name_lda=BOOKS_LDA,
            name_count_vectorizer=BOOKS_COUNT_VECTORIZER,
            MakerMatrixGenreClass=MakerMatrixGenre
    ):
        super(MakerMatrixBooks, self).__init__(name_matrix, columns_dummies, columns_select, name_lda,
                                               name_count_vectorizer)
        self.maker_matrix_genre = MakerMatrixGenreClass()

    def make(self, df, fit=True):
        df_genre = self.maker_matrix_genre.make(df.id)
        df_content, df_other = super(MakerMatrixBooks, self).make(df, fit=fit)
        return df_content, pd.concat([df_other, df_genre], axis=1)


class MakerMatrixEvents(MakerMatrixBase):
    def __init__(
            self,
            name_matrix=EVENTS,
            columns_dummies=['town', 'age_rate'],
            columns_select=['id'],
            name_lda=EVENTS_LDA,
            name_count_vectorizer=EVENTS_COUNT_VECTORIZER,
    ):
        super(MakerMatrixEvents, self).__init__(name_matrix, columns_dummies, columns_select, name_lda,
                                                name_count_vectorizer)


class MakerMatrixCulturalCenters(MakerMatrixBase):
    def __init__(
            self,
            name_matrix=CULTURAL_CENTERS,
            columns_dummies=['underground'],
            columns_select=['id', 'latitude', 'longitude'],
            name_lda=CULTURAL_CENTERS_LDA,
            name_count_vectorizer=CULTURAL_CENTERS_COUNT_VECTORIZER,
    ):
        super(MakerMatrixCulturalCenters, self).__init__(name_matrix, columns_dummies, columns_select, name_lda,
                                                         name_count_vectorizer)


class MakerMatrixLibraries(MakerMatrixBase):
    def __init__(
            self,
            name_matrix=LIBRARIES,
            columns_dummies=['region'],
            columns_select=['id', 'latitude', 'longitude'],
            name_lda=LIBRARIES_LDA,
            name_count_vectorizer=LIBRARIES_COUNT_VECTORIZER,
    ):
        super(MakerMatrixLibraries, self).__init__(name_matrix, columns_dummies, columns_select, name_lda,
                                                   name_count_vectorizer)


class MakerPreprocessingMatrixBase(MakerMatrix):
    def __init__(self, Object, MakerClass, select_columns, name_matrix, name_content, path_csv=PATH_DATA_CSV,
                 MakerMatrixForPreprocessingClass=MakerMatrixForPreprocessing):
        self.name_matrix = name_matrix
        self.select_columns = select_columns
        self.name_matrix = name_matrix
        self.path_csv = path_csv
        self.Object = Object
        self.MakerClass = MakerClass
        self.MakerMatrixForPreprocessingClass = MakerMatrixForPreprocessingClass
        self.name_content = name_content

    def make(self, save=True, fit=True):
        maker_matrix_for_preprocessing = self.MakerMatrixForPreprocessingClass(self.Object)
        df_for_preprocessing = maker_matrix_for_preprocessing.make(self.select_columns)
        maker_matrix = self.MakerClass()
        df_content, df_preprocessing = maker_matrix.make(df_for_preprocessing, fit=fit)

        if save:
            self.save_df(df_preprocessing, self.path_csv, self.name_matrix)
            self.save_df(df_content, self.path_csv, self.name_content)
        return df_content, df_preprocessing


class MakerMatrixPreprocessingBooks(MakerPreprocessingMatrixBase):
    def __init__(
            self,
            Object=Book,
            MakerClass=MakerMatrixBooks,
            select_columns=['id', 'author', 'pages', 'rating', 'language', 'content'],
            name_matrix=PREPROCESSING_BOOKS,
            name_content=PREPROCESSING_CONTENT_BOOKS,
    ):
        super(MakerMatrixPreprocessingBooks, self).__init__(Object, MakerClass, select_columns, name_matrix,
                                                            name_content)


class MakerMatrixPreprocessingEvents(MakerPreprocessingMatrixBase):
    def __init__(
            self,
            Object=Event,
            MakerClass=MakerMatrixEvents,
            select_columns=['id', 'town', 'price', 'age_rate', 'content'],
            name_matrix=PREPROCESSING_EVENTS,
            name_content=PREPROCESSING_CONTENT_EVENTS,
    ):
        super(MakerMatrixPreprocessingEvents, self).__init__(Object, MakerClass, select_columns, name_matrix,
                                                             name_content)


class MakerMatrixPreprocessingCulturalCenters(MakerPreprocessingMatrixBase):
    def __init__(
            self,
            Object=CultureCenter,
            MakerClass=MakerMatrixCulturalCenters,
            select_columns=['id', 'underground', 'latitude', 'longitude', 'content'],
            name_matrix=PREPROCESSING_CULTURAL_CENTERS,
            name_content=PREPROCESSING_CONTENT_CULTURAL_CENTERS,
    ):
        super(MakerMatrixPreprocessingCulturalCenters, self).__init__(Object, MakerClass, select_columns, name_matrix,
                                                                      name_content)


class MakerMatrixPreprocessingLibraries(MakerPreprocessingMatrixBase):
    def __init__(
            self,
            Object=Library,
            MakerClass=MakerMatrixLibraries,
            select_columns=['id', 'region', 'latitude', 'longitude', 'content'],
            name_matrix=PREPROCESSING_LIBRARIES,
            name_content=PREPROCESSING_CONTENT_LIBRARIES,
    ):
        super(MakerMatrixPreprocessingLibraries, self).__init__(Object, MakerClass, select_columns, name_matrix,
                                                                name_content)


class MakerSimilarJSONBase:
    def __init__(self, name_df, name_json, path_data=PATH_DATA_CSV, path_json=PATH_DATA_JSON):
        self.name_df = name_df
        self.path_data = path_data
        self.path_json = path_json
        self.name_json = name_json

    def make(self, save=True):
        df = pd.read_csv(self.path_data + self.name_df + '.csv')
        df_t = df.drop('id', axis=1)
        cosine_similarities = linear_kernel(df_t.values, df_t.values)
        results = {}
        for idx, row in tqdm(df.iterrows(), desc=self.name_df):
            similar_indices = cosine_similarities[idx].argsort()[::-1]
            similar_items = [int(df['id'][i]) for i in similar_indices]
            results[int(row['id'])] = similar_items[1:]

        if save:
            self.save_json(results)

        return results

    def save_json(self, data):
        with open(f"{self.path_json}{self.name_json}.json", "w") as write_file:
            json.dump(data, write_file)


class MakerSimilarJSONBooks(MakerSimilarJSONBase):
    def __init__(self, name_df=PREPROCESSING_BOOKS, name_json=SIMILAR_BOOKS):
        super(MakerSimilarJSONBooks, self).__init__(name_df, name_json)


class MakerSimilarJSONEvents(MakerSimilarJSONBase):
    def __init__(self, name_df=PREPROCESSING_EVENTS, name_json=SIMILAR_EVENTS):
        super(MakerSimilarJSONEvents, self).__init__(name_df, name_json)


class MakerSimilarJSONCulturalCenters(MakerSimilarJSONBase):
    def __init__(self, name_df=PREPROCESSING_CULTURAL_CENTERS, name_json=SIMILAR_CULTURAL_CENTERS):
        super(MakerSimilarJSONCulturalCenters, self).__init__(name_df, name_json)


class MakerFilteringModelBase:
    def __init__(self, name_df, name_model, path_data=PATH_DATA_CSV, path_model=PATH_MODELS):
        self.name_df = name_df
        self.name_model = name_model
        self.path_data = path_data
        self.path_model = path_model

    def make(self, save=True):
        df = pd.read_csv(self.path_data + self.name_df + '.csv')
        df = df.drop('id', axis=1)
        matrix = csr_matrix(df.values)
        model = LightFM(loss='warp')
        model.fit(matrix)
        if save:
            dump(model, f'{self.path_model}{self.name_model}.joblib')
        return model


class MakerFilteringModelBooks(MakerFilteringModelBase):
    def __init__(self, name_df=FILTER_MATRIX_USERS_BOOKS, name_model=FILTERING_MODEL_BOOKS):
        super(MakerFilteringModelBooks, self).__init__(name_df, name_model)


class MakerFilteringModelEvents(MakerFilteringModelBase):
    def __init__(self, name_df=FILTER_MATRIX_USERS_EVENTS, name_model=FILTERING_MODEL_EVENTS):
        super(MakerFilteringModelEvents, self).__init__(name_df, name_model)


class MakerFilteringModelCulturalCenters(MakerFilteringModelBase):
    def __init__(self, name_df=FILTER_MATRIX_USERS_CULTURAL_CENTERS, name_model=FILTERING_MODEL_CULTURAL_CENTERS):
        super(MakerFilteringModelCulturalCenters, self).__init__(name_df, name_model)
