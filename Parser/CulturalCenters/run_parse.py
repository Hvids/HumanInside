from ParserPage import ParserUrlsCulturalCenters, ParserCulturalCenters

site = 'https://www.2do2go.ru'
url_start_page = 'https://www.2do2go.ru/msk/kulturnye-centry'
postfix = '?offset='
range_postfix = [1, 37]


parser_start_page = ParserUrlsCulturalCenters(site, url_start_page, postfix, range_postfix)
urls_cultural_centers = parser_start_page.urls

parser_cultural_centers = ParserCulturalCenters(site, urls_cultural_centers)
cultural_centers = parser_cultural_centers.cultural_centers

path_pd = '../../data/csv'

print('save_csv')
cultural_centers.save(path_pd)
