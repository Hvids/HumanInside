import sys
sys.path.append('../')
from ParserPage import ParserUrlsCulturalCenters

site = 'https://www.2do2go.ru'
url_start_page = 'https://www.2do2go.ru/msk/kulturnye-centry'
postfix = '?offset='
range_postfix = [1, 2]

parser_start_page = ParserUrlsCulturalCenters(site, url_start_page, postfix, range_postfix)
urls_cultural_centers = parser_start_page.urls
print(urls_cultural_centers)