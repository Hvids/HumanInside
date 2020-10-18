import sys

from PreProcessing import PreProcessingGenre, PreProcessingContent, PreProcessingDummies, PreProcessingGropColumns
import pandas as pd
path = '../data/csv/'
name = 'books.csv'
name_save = 'preprocessing_books.csv'
full_name_save =path+ name_save
full_name = path+ name

df_books = pd.read_csv(full_name)

df_books.content = df_books.content.fillna('')

genre = df_books.genre
content = df_books.content
author = df_books.author
language = df_books.language

preprocessing_genre =PreProcessingGenre()
preprocessing_drop = PreProcessingDropColumns()
preprocessing_dum = PreProcessingDummies()
preprocessing_content = PreProcessingContent()

df_genre = preprocessing_genre.make(genre)
df_content_lda = preprocessing_content.make_matrix_lda_with_load(content)
df_content_w2v = preprocessing_content.make_matrix_w2v(content)
df_author = preprocessing_dum.make(author)
df_laguage = preprocessing_dum.make(language)

columns_drop = ['name', 'author','genre', 'seria','language','content','img_url']
df_books =preprocessing_drop.make(df_books,columns_drop)
df_preprocessing_result_books = pd.concat([df_books,df_genre,df_content_lda,df_content_w2v,df_author,df_laguage],axis=1)
df_preprocessing_result_books.to_csv(full_name_save, index=False)
