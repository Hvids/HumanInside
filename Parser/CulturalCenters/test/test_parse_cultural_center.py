import  sys
sys.path.append('../')
sys.path.append('../../')
from ParserPage import  ParserCulturalCenter
url = 'https://www.2do2go.ru/places/35155/kulturnyy-centr-vdohnovenie'
# url = 'https://www.2do2go.ru/places/52999/kulturno-informacionnyi-centr-leonidovka'
# url = 'https://www.2do2go.ru/places/46978/mnogofunkcionalnyi-kulturnyi-centr'
# url = 'https://www.2do2go.ru/places/35461/kulturnyi-centr-pokrovskie-vorota'
site = 'https://www.2do2go.ru'

pc = ParserCulturalCenter(site,url)
cc = pc.parse_center(1)
print(cc)
path_pd = '../../../data/csv'
path_img_cultural_center = '../../../data/img/cultural_centers/'
path_img_event = '../../../data/img/events/'

#