import sys

sys.path.extend(['../', '../../'])

from Parser import ParserUrls, ParserDataList, ParserData
from Library import Libraries, Library

class ParserLibrary(ParserData):
    name = 'Parser Library'

    @property
    def img_url(self):
        reg = r'<div class="cover_image-wrap cover_image-wrap__blur"><div style="background-image:url\((.*?)\)" class="cover_image">'
        img_url = self.parser_img(reg)
        return img_url

    @property
    def content(self):
        reg = r'<div class="styled-content_body">(.*?)<span class="clearfix"></span></div>'
        content = self.parse_content(reg)
        return content

    @property
    def social_networks(self):
        reg = r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Социальные сети</span>: </div><div class="attributes_value">(.*?)</div></div>'
        social_networks = self.parse_social_networks(reg)
        return  social_networks
    def parse(self, id):
        regs = {
            'name':r'<h1 class="entity-heading_title">(.*?)</h1>',
            'type': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Тип места</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'region': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Регион</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'location': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Местоположение</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'adress': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Адрес</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'latitude': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Широта</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'longitude': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Долгота</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'number': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Телефон</span>: </div><div class="attributes_value"><div class="attributes_value">(.*?)</div></div></div>',
            'site': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Сайт</span>: </div><a href="(.*?)" target="blank" rel="nofollow" class="attributes_value">',
            'email': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Email</span>: </div><a href="mailto:(.*?)" target="blank" rel="nofollow" class="attributes_value">',
            'time_work': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Часы работы</span>: </div><div class="attributes_value">(.*?)</div></div>'

        }
        passport = self.text.parse_passport(regs)
        passport['social_networks'] = self.social_networks
        passport['content'] = self.content
        passport['img_url'] = self.img_url
        return Library(passport)

class ParserLibraries(ParserDataList):
    name = 'Parser Libraries'

    @property
    def libraries(self):
        libraries_obj = Libraries
        parse_library_obj = ParserLibrary
        libraries = self.parse(libraries_obj, parse_library_obj)
        return libraries


class ParserUrlsLibrary(ParserUrls):
    name = 'ParserUrlsLibrary'
    def get_urls(self, range_postfix):
        reg = r'<div class="entity-card-v2_body"><a href="(.*?)" class="card-cover">'
        urls = self.parse(reg, range_postfix)
        return urls
