import  sys
sys.path.append('../')

import pandas as pd
from Img import SaverImgs

path_pd_ev = '../../data/csv/events.csv'
path_pd_cc = '../../data/csv/cultural_centers.csv'

path_img_cultural_center = '../../data/img/cultural_centers/'
path_img_event = '../../data/img/events/'

data_ev = pd.read_csv(path_pd_ev)
data_cc = pd.read_csv(path_pd_cc)


saver_imgs_cc = SaverImgs(data_cc.id,data_cc.img_url)
saver_imgs_cc.save(path_img_cultural_center)


saver_imgs_ev = SaverImgs(data_ev.id, data_ev.img_url)
saver_imgs_ev.save(path_img_event)
