import  sys

sys.path.extend(['../','../../'])
prefix = 'https://www.litmir.me'
url = '/bs?rs=5%7C1%7C0'
postfix= '&o=10&p='


from ParserPage import ParserUrlsBook, ParserBooks

range_postfix = [1, 2]
parser_urls = ParserUrlsBook(prefix,url,postfix)
urls = parser_urls.get_urls(range_postfix)

parser_books = ParserBooks(prefix,urls)
book = parser_books.books