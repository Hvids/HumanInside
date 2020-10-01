import  sys
sys.path.append('../')

import pandas as pd
from Img import SaverImgs

path_pd = '../../data/csv/libraries.csv'

path_img = '../../data/img/libraries/'

data = pd.read_csv(path_pd)

saver_imgs = SaverImgs(data.id,data.img_url)
saver_imgs.save(path_img)

