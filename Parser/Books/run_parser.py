import  sys

sys.path.extend(['../','../../'])
prefix = 'https://www.litmir.me'
url = '/bs?rs=5%7C1%7C0'
postfix= '&o=100&p='


from ParserPage import ParserUrlsBook, ParserBooks

range_postfix = [1, 6223]
parser_urls = ParserUrlsBook(prefix,url,postfix)
urls = parser_urls.get_urls(range_postfix)

parser_books = ParserBooks(prefix,urls)

book = parser_books.books

path_pd = '../../../data/csv'
print('save')
book.save(path_pd)