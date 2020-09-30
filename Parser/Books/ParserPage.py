import sys

sys.path.append('../')

from Parser import ParserUrls, ParserDataList, ParserData, Parser
from Book import Book, Books
from Comment import Comment, Comments


class ParserComment:
    def __init__(self, text):
        self.text = text

    @property
    def date(self):
        reg = r'<meta itemprop="datePublished" content="(.*?)">'
        data_ = Parser.get_str_by_reg(reg, self.text)
        return data_

    @property
    def rating(self):
        reg = r'<span itemprop="ratingValue">(.*?)</span>'
        res = Parser.get_str_by_reg(reg, self.text)
        return res

    @property
    def content(self):
        reg = '<span itemprop="reviewBody">(.*?)</span>'
        res = Parser.get_str_by_reg(reg, self.text)
        return res

    def parse_comment(self, id_book):
        date = self.date
        rating = self.rating
        content = self.content
        return Comment(id_book, date, rating, content)


class ParserComments(ParserData):
    def parse_comments(self, id_book):
        comments_obj = Comments()
        reg = r'<table jq="CommentBlock".*'
        comments_text = self.text.findall(reg)
        for comment in comments_text:
            parser_comment = ParserComment(comment)
            comment_obj = parser_comment.parse_comment(id_book)
            if comment_obj.rating == '':
                continue
            print(f'com = {comment_obj.id} {comment_obj.date}')
            comments_obj.add(comment_obj)
        return comments_obj


class ParserBook(ParserData):
    @property
    def img_url(self):
        reg = r'<img jq="BookCover" itemprop="image" class=".*?" width=".*?" height=".*?" alt=".*?" src="(.*?)" '
        img_url = self.text.get_str_by_reg(reg)
        img_url = self.site + img_url
        return img_url

    def parse_comments(self, id_book):
        parser_comments = ParserComments(self.site, self.url)
        comments_ = parser_comments.parse_comments(id_book)
        return comments_

    @property
    def content(self):
        reg = r'<div itemprop="description" jq="BookAnnotationText".*?>(.*?)</div>'
        content = self.text.get_str_by_reg(reg)
        reg = r'<p>(.*?)</p>'
        content = Parser.get_str_by_reg(reg, content)
        return content

    def parse_passport(self, regs):
        passport = {}
        for key in regs.keys():
            passport[key] = self.text.get_str_by_reg(regs[key])
        return passport

    def parse_book(self, id_book):
        regs = {
            'name': r'<div itemprop="name" class="lt35" style="float:left;">(.*?)</div>',
            'author': r'<meta itemprop="name" content="(.*?)">',
            'genre': r'<span itemprop="genre">(.*?)</span>',
            'seria': r'<a href="/books_in_series/.*?">(.*?)</a>',
            'rating': r'<span itemprop="ratingValue" class="orange_desc">(.*?)</span>',
            'count_page': r'<span itemprop="numberOfPages" class="desc2">(.*?)</span>',
            'language': r'<span itemprop="inLanguage" class="desc2">(.*?)</span>'

        }
        # comments = self.parse_comments(id_book)
        passport = self.parse_passport(regs)
        passport['content'] = self.content
        passport['img_url'] = self.img_url
        # book_ = Book(id_book, passport, comments)
        book_ = Book(id_book, passport)
        return book_


class ParserBooks(ParserDataList):

    @property
    def books(self):
        books = Books()
        for id_book, url in enumerate(self.urls):
            parser_book = ParserBook(self.site, url)
            book = parser_book.parse_book(id_book)
            print(f"{id_book} {book.passport['name']}")
            books.add(book)
        return books


class ParserUrlsBook(ParserUrls):
    def get_urls(self, range_postfix):
        reg = r'<div class="book_name"><a href="(.*?)">'
        urls = self.parse(reg, range_postfix)
        return urls
