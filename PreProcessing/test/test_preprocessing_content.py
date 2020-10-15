import sys
sys.path.append('../')
from PreProcessing import PreProcessingGenre, PreProcessingContent
import pandas as pd
path = '../../data/csv/'
name = 'books.csv'
full_name = path+ name

df_books = pd.read_csv(full_name)

content = df_books.content

content = content.fillna('')

preprocessing_content = PreProcessingContent(content)
content = preprocessing_content.make()