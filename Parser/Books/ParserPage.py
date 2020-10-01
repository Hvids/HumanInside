import sys

sys.path.extend(['../'])

from Parser import ParserUrls, ParserDataList, ParserData
from Book import Book, Books


class ParserBook(ParserData):
    @property
    def img_url(self):
        reg = r'<img jq="BookCover" itemprop="image" class=".*?" width=".*?" height=".*?" alt=".*?" src="(.*?)" '
        img_url = self.parser_img(reg)
        return img_url

    @property
    def content(self):
        reg = r'<div itemprop="description" jq="BookAnnotationText".*?>(.*?)</div>'
        content = self.parse_content(reg)
        return content

    def parse(self,id):
        regs = {
            'name': r'<div itemprop="name" class="lt35" style="float:left;">(.*?)</div>',
            'author': r'<meta itemprop="name" content="(.*?)">',
            'genre': r'<span itemprop="genre">(.*?)</span>',
            'seria': r'<a href="/books_in_series/.*?">(.*?)</a>',
            'rating': r'<span itemprop="ratingValue" class="orange_desc">(.*?)</span>',
            'count_page': r'<span itemprop="numberOfPages" class="desc2">(.*?)</span>',
            'language': r'<span itemprop="inLanguage" class="desc2">(.*?)</span>'

        }

        passport = self.text.parse_passport(regs)
        passport['content'] = self.content
        passport['img_url'] = self.img_url

        book_ = Book(passport)
        return book_


class ParserBooks(ParserDataList):
    name = 'Parser Books'

    @property
    def books(self):
        books_obj = Books
        parse_book_obj = ParserBook
        books = self.parse(books_obj, parse_book_obj)
        return books


class ParserUrlsBook(ParserUrls):
    name = 'Parser Urls'

    def get_urls(self, range_postfix):
        reg = r'<div class="book_name"><a href="(.*?)">'
        urls = self.parse(reg, range_postfix)
        return urls
