import sys
sys.path.append('../../')
sys.path.append('../')
import  pandas as pd

path_pd_ev = '../../../data/csv/events.csv'
path_pd_cc = '../../../data/csv/cultural_centers.csv'

path_img_cultural_center = '../../../data/img/cultural_centers/'
path_img_event = '../../../data/img/events/'

data_ev = pd.read_csv(path_pd_ev)
data_cc = pd.read_csv(path_pd_cc)

from Img import  SaverImgs

saver_imgs_ev = SaverImgs(data_ev.id,data_ev.img_url)
saver_imgs_ev.save(path_img_event)