import sys

from PreProcessing import PreProcessingGenre, PreProcessingContent, PreProcessingDummies, PreProcessingGropColumns
import pandas as pd

path = '../data/csv/'
name = 'events.csv'
name_save = 'preprocessing_events.csv'
full_name_save = path + name_save
full_name = path + name

df_events = pd.read_csv(full_name)

df_events.content = df_events.content.fillna('')
df_events.price = df_events.price.fillna(0)

content = df_events.content
age = df_events.age
town = df_events.town

columns_drop = ['name', 'site_buy', 'date', 'town', 'age', 'img_url', 'content', 'id_cultural']

preprocessing_drop = PreProcessingGropColumns()
preprocessing_dum = PreProcessingDummies()
preprocessing_content = PreProcessingContent()

df_content_lda = preprocessing_content.make_matrix_lda_with_load(content)
df_content_w2v = preprocessing_content.make_matrix_w2v(content)
df_age = preprocessing_dum.make(age)
df_town = preprocessing_dum.make(town)
df_cultural_centers = preprocessing_drop.make(df_events, columns_drop)

df_preprocessing_result_books = pd.concat(
    [df_cultural_centers, df_content_lda, df_content_w2v, df_age, df_cultural_centers],
    axis=1)
df_preprocessing_result_books.to_csv(full_name_save, index=False)
