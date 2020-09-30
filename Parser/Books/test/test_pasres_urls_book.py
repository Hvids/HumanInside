import  sys
sys.path.extend(['../','../../'])

from ParserPage import ParserUrlsBook

site = 'https://www.litmir.me'
url = '/bs?rs=5%7C1%7C0'
postfix = '&o=100&p='
range_postfix = [1, 2]

parser_urls = ParserUrlsBook(site,url,postfix)
print(parser_urls.get_urls(range_postfix))