from .Maker import MakerMatrixBooks, MakerMatrixEvents, MakerMatrixPreprocessingBooks, \
    MakerMatrixPreprocessingEvents, MakerMatrixPreprocessingEvents
import pandas as pd
from .paths import *
from .names import *
from sklearn.metrics.pairwise import linear_kernel
from tqdm import tqdm
from polls.models import *


class RequestModelBase:
    def __init__(self, SelectObject, id_name, MakerMatrixClass, df, k=5):
        self.df = df
        self.k = k
        self.id_name = id_name
        self.maker_matrix = MakerMatrixClass()
        self.SelectObject = SelectObject

    @staticmethod
    def load_df(path, name):
        return pd.read_csv(f'{path}{name}.csv')

    @staticmethod
    def get_list(tuple_list):
        return [t[0] for t in tuple_list]

    def recommend(self, id_user, text):
        df_text = pd.DataFrame([text], columns=['content'])
        objects_read_user = self.SelectObject.objects.filter(id_user=id_user).order_by('-id').values_list(self.id_name)
        objects_read_user = self.get_list(objects_read_user)
        content = self.maker_matrix.make_content(df_text, fit=False)
        cosine_similarities = linear_kernel(content.values, self.df.drop('id', axis=1).values)
        similar_indices = cosine_similarities[0].argsort()[::-1]
        similar_items = [int(self.df['id'][i]) for i in similar_indices if int(self.df['id'][i])]
        results = similar_items[1:]
        results = [int(i) for i in results if int(i) not in objects_read_user]
        return results[:self.k]

    def update_with_maker(self, maker):
        maker.make()


class RequestModelBooks(RequestModelBase):
    @classmethod
    def load(
            cls,
            SelectObject=LastBook,
            id_name='id_book',
            MakreMatrixClass=MakerMatrixBooks,
            name=PREPROCESSING_CONTENT_BOOKS,
            path=PATH_DATA_CSV,
            k=5
    ):
        df = cls.load_df(path, name)
        return cls(SelectObject=SelectObject, id_name=id_name, MakerMatrixClass=MakreMatrixClass, df=df, k=k)

    def update(self, k=5, maker=MakerMatrixPreprocessingBooks):
        self.update_with_maker(maker)
        return RequestModelBooks.load(k=k)


class RequestModelEvents(RequestModelBase):
    @classmethod
    def load(
            cls,
            SelectObject=LastEvent,
            id_name='id_event',
            MakreMatrixClass=MakerMatrixEvents,
            name=PREPROCESSING_CONTENT_EVENTS,
            path=PATH_DATA_CSV,
            k=5
    ):
        df = cls.load_df(path, name)
        return cls(SelectObject=SelectObject, id_name=id_name, MakerMatrixClass=MakreMatrixClass, df=df, k=k)

    def update(self, k=5, maker=MakerMatrixPreprocessingEvents):
        self.update_with_maker(maker)
        return RequestModelBooks.load(k=k)


# from recommendation_system.RequestModels import  RequestModelBooks; r = RequestModelBooks.load(); пг
