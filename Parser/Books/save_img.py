import  sys
sys.path.append('../')

import pandas as pd
from Img import SaverImgs

path_pd_books = '../../data/csv/books.csv'


path_img_book = '../../data/img/books/'


df = pd.read_csv(path_pd_books)


print("save cc img")
saver = SaverImgs(df.id,df.img_url)
saver.save(path_img_book)

