import pandas as pd
from joblib import dump, load
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import numpy as np
from tqdm import tqdm
import pymorphy2
from nltk.tokenize import TweetTokenizer
import gensim.downloader as api
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
# import nltk

# nltk.download("stopwords")
# --------#

from nltk.corpus import stopwords

from string import punctuation


class PreProcessing:
    def __init__(self, column):
        self.column = list(column)

    def make(self):
        pass


class PreProcessingGenre:
    def make(self, genres):
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


class PreProcessingDummies:
    # подаем значение колонки которую делаем дамми
    def make(self, column):
        df = pd.get_dummies(column)
        return df


class PreProcessingLabelEncoding(PreProcessing):
    # Значение колонок которые енкодим
    def make(self, column):
        label_encoding = LabelEncoder()
        column = label_encoding.fit_transform(column)
        return column


class PreProcessingGropColumns:
    # Column - название колонок которые удаляем, df - откуда удалять
    def make(self, df, columns):
        columns_name_drop = columns
        df = df.drop(columns_name_drop, axis=1)
        return df


class PreProcessingScaler(PreProcessing):
    def make(self, columns):
        scaler = StandardScaler()
        res = scaler.fit_transform(columns)
        return res


class PreProcessingText:
    def __init__(self):
        self.model_w2v = api.load("word2vec-ruscorpora-300")
        self.morph = pymorphy2.MorphAnalyzer()
        self.tkns = TweetTokenizer()
        self.russian_stopwords = stopwords.words("russian")

    def make_vector(self, text):
        tokens = self.tkns.tokenize(text)
        size_vector = self.model_w2v.vector_size
        vector = np.zeros(shape=size_vector)
        for token in tokens:
            try:
                vector += np.array(self.model_w2v.wv[token])
            except:
                pass
        vector = vector if len(tokens) == 0 else vector
        return list(vector)

    def make_token(self, word):
        processed = self.morph.parse(word)[0]
        normal_phorm = processed.normal_form
        tag = str(processed.tag).split(',')[0]
        return normal_phorm + '_' + tag

    def make_preprocess_text(self, text):
        tokens = self.tkns.tokenize(text.lower())
        tokens = [self.make_token(token) for token in tokens if token not in self.russian_stopwords \
                  and token.strip() not in punctuation
                  and token not in ['–', '«', '…', '—', '»', '', ' ']
                  and not token.isdigit()
                  ]

        text = " ".join(tokens)

        return text

    def make_w2v(self, content):
        text = self.make_preprocess_text(content)
        vectror = self.make_vector(text)
        return vectror


class PreProcessingContent:
    name = 'PreProcessingContent'

    def __init__(self, path_models='./models/'):
        self.path_models = path_models
        self.preprocessing_text = PreProcessingText(path_models)

        self.lda_fitter = LatentDirichletAllocation(n_components=100,
                                                    max_iter=30,
                                                    n_jobs=6,
                                                    learning_method='batch',
                                                    verbose=1)
        self.count_vectorizer_fitter = CountVectorizer()

        self.count_vectorizer_loder = load(f'{path_models}count_vectorizer.joblib')
        self.lda_loder = load(f'{path_models}lda.joblib')

    def make_matrix_w2v(self, contents):
        res_contents = []
        for content in tqdm(contents, desc=self.name):
            content_new = self.preprocessing_text.make_w2v(content)
            res_contents.append(content_new)
        return pd.DataFrame(res_contents)

    def make_matrix_lda_with_fit(self, contents):
        res_contents = []
        for content in tqdm(contents, desc=self.name):
            content_new = self.preprocessing_text.make_preprocess_text(content)
            res_contents.append(content_new)
        self.fit_count_vectorizer(res_contents)
        res_contents = self.count_vectorizer_fitter.transform(res_contents)
        self.fit_lda(res_contents)
        return pd.DataFrame(self.lda_fitter.transform(res_contents))

    def make_matrix_lda_with_load(self, contents):
        res_contents = []
        for content in tqdm(contents, desc=self.name):
            content_new = self.preprocessing_text.make_preprocess_text(content)
            res_contents.append(content_new)
        res_contents = self.count_vectorizer_loder.transform(res_contents)
        return pd.DataFrame(self.lda_loder.transform(res_contents))

    def fit_count_vectorizer(self, contents):
        self.count_vectorizer_fitter.fit(contents)
        dump(self.count_vectorizer_fitter, f'{self.path_models}count_vectorizer.joblib')

    def fit_lda(self, contents):
        self.lda_fitter.fit(contents)
        dump(self.lda_fitter, f'{self.path_models}lda.joblib')
