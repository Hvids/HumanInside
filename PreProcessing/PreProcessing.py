import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
from gensim.models.phrases import Phrases, Phraser
import nltk
# nltk.download("stopwords")
# --------#

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation


class PreProcessing:
    def __init__(self, column):
        self.column = list(column)

    def make(self):
        pass


class PreProcessingGenre(PreProcessing):
    """
    В конструтор подается колонка жанров, значение
    """

    def make(self):
        genres = self.column
        genres_set = set('')
        genres_books = []
        # Сделать множество всех жанров и списко жанров для каждой книги
        for genres_book_str in genres:
            genres_book_list = []
            genres_book_words_list = genres_book_str.split(' ')

            if list(genres_book_words_list) == 0:
                genres_book_list.append('')
                continue

            genre_name = genres_book_words_list[0]

            for word in genres_book_words_list:
                if word[0].isupper():
                    genres_book_list.append(genre_name)
                    genres_set.add(genre_name)
                    genre_name = word
                else:
                    genre_name += ' ' + word
            genres_book_list.append(genre_name)
            genres_set.add(genre_name)
            genres_books.append(genres_book_list)

        columns = list(genres_set)
        # Сделать df для жанров тип one hot encoding
        df_genre = pd.DataFrame(columns=columns)
        for genres_book in genres_books:
            row_val = [1 if genre in genres_book else 0 for genre in columns]
            row = dict(zip(columns, row_val))
            df_genre = df_genre.append(row, ignore_index=True)
        return df_genre


class PreProcessingDummies(PreProcessing):
    # подаем значение колонки которую делаем дамми
    def make(self):
        df = pd.get_dummies(self.column)
        return df


class PreProcessingLabelEncoding(PreProcessing):
    # Значение колонок которые енкодим
    def make(self):
        label_encoding = LabelEncoder()
        columns = label_encoding.fit_transform(self.column)
        return columns


class PreProcessingGropColumns(PreProcessing):
    # Column - название колонок которые удаляем, df - откуда удалять
    def make(self, df):
        columns_name_drop = self.column
        df = df.drop(columns_name_drop, axis=1)
        return df


class PreProcessingScaler(PreProcessing):
    def make(self):
        scaler = StandardScaler()
        res = scaler.fit_transform(self.column)
        return res


class PreProcessingText(PreProcessing):
    def __init__(self, text):
        self.text = text

        self.mystem = Mystem()
        self.russian_stopwords = stopwords.words("russian")


    def preprocess_text(self):

        tokens = self.mystem.lemmatize(self.text.lower())
        tokens = [token for token in tokens if token not in self.russian_stopwords \
                  and token != " " \
                  and token.strip() not in punctuation
                  and token not ['–', '«', '…', '—', '»']
                  ]

        text = " ".join(tokens)

        return text


    def make(self):
        text = self.preprocess_text()
        return text


class PreProcessingContent(PreProcessing):
    name = 'PreProcessingContent'
    def make(self):
        contents = self.column
        res_contents = []
        for content in tqdm(contents, desc=self.name):
            preprocessing_text = PreProcessingText(content)
            content_new = preprocessing_text.make()
            res_contents.append(content_new)
        return res_contents
