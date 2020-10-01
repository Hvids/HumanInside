import sys

sys.path.extend(['../'])

from ParserPage import ParserUrlsLibrary, ParserLibraries

url = 'https://www.culture.ru/literature/libraries/location-moskva'
site = 'https://www.culture.ru'
postfix = '?page='
range_page = (1, 2)

parser_urls = ParserUrlsLibrary(site, url, postfix)
urls = parser_urls.get_urls(range_page)

parser_books = ParserLibraries(site,urls)

libs = parser_books.libraries
path_pd = '../../data/csv/'
libs.save(path_pd)