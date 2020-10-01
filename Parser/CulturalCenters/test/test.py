import  sys

sys.path.extend(['../','../../'])
site = 'https://www.2do2go.ru'
url = 'https://www.2do2go.ru/msk/kulturnye-centry'
postfix = '?offset='

from ParserPage import ParserUrlsCulturalCenters, ParserCulturalCenters

range_postfix = [1, 2]
parser_urls = ParserUrlsCulturalCenters(site,url,postfix)
urls = parser_urls.get_urls(range_postfix)

parser = ParserCulturalCenters(site,urls)

ccs = parser.cultural_centers
print(ccs)
print(ccs.data_list[0].events)

