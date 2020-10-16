import sys

from PreProcessing import PreProcessingGenre, PreProcessingContent, PreProcessingDummies, PreProcessingGropColumns
import pandas as pd

path = '../data/csv/'
name = 'cultural_centers.csv'
name_save = 'preprocessing_cultural_centers.csv'
full_name_save = path + name_save
full_name = path + name

df_cultural_centers = pd.read_csv(full_name)

df_cultural_centers.content = df_cultural_centers.content.fillna('')
df_cultural_centers.undegroud = df_cultural_centers.undegroud.fillna('')
df_cultural_centers.latitude = df_cultural_centers.latitude.fillna(0)
df_cultural_centers.logitute = df_cultural_centers.logitute.fillna(0)

content = df_cultural_centers.content
undegroud = df_cultural_centers.undegroud

columns_drop = ['name', 'offical_site', 'undegroud', 'adress', 'number', 'email', 'content', 'img_url',
                'social_netwoks']

preprocessing_drop = PreProcessingGropColumns()
preprocessing_dum = PreProcessingDummies()
preprocessing_content = PreProcessingContent()

df_content_lda = preprocessing_content.make_matrix_lda_with_load(content)
df_content_w2v = preprocessing_content.make_matrix_w2v(content)
df_undegroud = preprocessing_dum.make(undegroud)

df_cultural_centers = preprocessing_drop.make(df_cultural_centers, columns_drop)
df_preprocessing_result_books = pd.concat([df_cultural_centers, df_content_lda, df_content_w2v, df_undegroud],
                                          axis=1)
df_preprocessing_result_books.to_csv(full_name_save, index=False)
