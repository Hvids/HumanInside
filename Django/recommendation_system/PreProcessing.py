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
from .paths import *
import nltk

nltk.download("stopwords")
# --------#

from nltk.corpus import stopwords

from string import punctuation


class PreProcessing:
    def __init__(self, column):
        self.column = list(column)

    def make(self):
        pass


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


class PreProcessingDropColumns:
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
        self.texts = None

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

    def __init__(self, name, name_lda, name_count_vectorizer, path_models=PATH_MODELS):
        self.name = name
        self.name_lda = name_lda
        self.name_count_vectorizer = name_count_vectorizer
        self.path_models = path_models
        self.preprocessing_text = PreProcessingText()

        self.lda_fitter = LatentDirichletAllocation(n_components=100,
                                                    max_iter=30,
                                                    learning_method='batch',
                                                    verbose=1)
        self.count_vectorizer_fitter = CountVectorizer()

        self.count_vectorizer_loder = load(f'{self.path_models}{self.name_count_vectorizer}.joblib')
        self.lda_loder = load(f'{self.path_models}{self.name_lda}.joblib')

    def make_matrix_w2v(self, contents):
        res_contents = []
        for content in tqdm(contents, desc=self.name + '_w2v'):
            content_new = self.preprocessing_text.make_w2v(content)
            res_contents.append(content_new)
        return pd.DataFrame(res_contents)

    def make_matrix_lda_with_fit(self, contents):
        print('Lda Fit')
        res_contents = []
        for content in tqdm(contents, desc=self.name + '_lda'):
            content_new = self.preprocessing_text.make_preprocess_text(content)
            res_contents.append(content_new)
        self.fit_count_vectorizer(res_contents)
        res_contents = self.count_vectorizer_fitter.transform(res_contents)
        self.fit_lda(res_contents)
        return pd.DataFrame(self.lda_fitter.transform(res_contents))

    def make_matrix_lda_with_load(self, contents):
        res_contents = []
        for content in tqdm(contents, desc=self.name + '_lda'):
            content_new = self.preprocessing_text.make_preprocess_text(content)
            res_contents.append(content_new)
        res_contents = self.count_vectorizer_loder.transform(res_contents)

        return pd.DataFrame(self.lda_loder.transform(res_contents))

    def fit_count_vectorizer(self, contents):
        self.count_vectorizer_fitter.fit(contents)
        dump(self.count_vectorizer_fitter, f'{self.path_models}{self.name_count_vectorizer}.joblib')

    def fit_lda(self, contents):
        self.lda_fitter.fit(contents)
        dump(self.lda_fitter, f'{self.path_models}{self.name_lda}.joblib')
