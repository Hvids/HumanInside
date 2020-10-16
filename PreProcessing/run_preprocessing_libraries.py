import sys

from PreProcessing import PreProcessingGenre, PreProcessingContent, PreProcessingDummies, PreProcessingGropColumns
import pandas as pd

path = '../data/csv/'
name = 'libraries.csv'
name_save = 'preprocessing_libraries.csv'
full_name_save = path + name_save
full_name = path + name

df_libraries = pd.read_csv(full_name)

df_libraries.content = df_libraries.content.fillna('')

content = df_libraries.content
type = df_libraries.type
location = df_libraries.location

preprocessing_drop = PreProcessingGropColumns()
preprocessing_dum = PreProcessingDummies()
preprocessing_content = PreProcessingContent()

columns_drop = ['name', 'type', 'region', 'location', 'adress', 'number', 'site', 'email', 'content', 'img_url','social_networks','time_work']

df_content_lda = preprocessing_content.make_matrix_lda_with_load(content)
df_content_w2v = preprocessing_content.make_matrix_w2v(content)
df_type = preprocessing_dum.make(type)
df_location = preprocessing_dum.make(location)

df_libraries = preprocessing_drop.make(df_libraries, columns_drop)
df_preprocessing_result_books = pd.concat([df_libraries, df_content_lda, df_content_w2v, df_location, df_type],
                                          axis=1)
df_preprocessing_result_books.to_csv(full_name_save, index=False)
