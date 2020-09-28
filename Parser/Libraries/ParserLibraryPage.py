import sys

sys.path.append('../')
import requests
import re
from Library import Library
from Parser import Parser

from bs4 import BeautifulSoup

class ParserLibraryPage(Parser):

    def __init__(self, url):
        self.url = url
        self.text = requests.get(url).text

    def parse(self):
        library = self.__get_library()
        return library

    def __get_passport(self):
        passport_value = {}

        reg_text = r'<div class="attributes attributes__modal">(.*?)</div></div></div></div>'
        text = self.get_str_by_reg(reg_text, self.text) + '</div></div>'

        regs = {
            'type': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Тип места</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'region': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Регион</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'location': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Местоположение</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'adress': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Адрес</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'latitude': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Широта</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'longitude': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Долгота</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'number': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Телефон</span>: </div><div class="attributes_value"><div class="attributes_value">(.*?)</div></div></div>',
            'site': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Сайт</span>: </div><a href="(.*?)" target="blank" rel="nofollow" class="attributes_value">',
            'email': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Email</span>: </div><a href="mailto:(.*?)" target="blank" rel="nofollow" class="attributes_value">',
            'social_networks': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Социальные сети</span>: </div><div class="attributes_value">(.*?)</div></div>',
            'time_work': r'<div class="attributes_block"><div class="attributes_label"><span class="text text__underline">Часы работы</span>: </div><div class="attributes_value">(.*?)</div></div>'
        }
        for key in regs.keys():
            if key == 'social_networks':
                reg_soc_network_links = regs[key]
                text_social_networks = self.get_str_by_reg(reg_soc_network_links, text)

                reg_social_networks = r'<a href="(.*?)" target="blank" rel="nofollow" class="attributes_value">'
                passport_value[key] = self.get_str_by_reg(reg_social_networks, text_social_networks)

                continue
            reg = regs[key]
            passport_value[key] = self.get_str_by_reg(reg, text)

        return passport_value

    def __get_name(self):
        reg = r'<h1 class="entity-heading_title">(.*?)</h1>'
        name = self.get_str_by_reg(reg, self.text)
        return name

    def __get_img_url(self):
        reg = r'<div class="cover_image-wrap cover_image-wrap__blur"><div style="background-image:url\((.*?)\)" class="cover_image">'
        img_url = self.get_str_by_reg(reg, self.text)
        return img_url

    def __get_content(self):
        reg_content_text = r'<div class="styled-content_body">(.*?)<span class="clearfix"></span></div>'
        content_text = self.get_str_by_reg(reg_content_text, self.text)
        reg_all_text = r'<p>(.*?)</p>'
        content_all_text = self.get_str_by_reg(reg_all_text, content_text) + '</end_str>'
        reg_text_main = r'</span>(.*?)</end_str>'
        reg_char = r'<span class="initial-letter">(.*?)</span>'
        content = self.get_str_by_reg(reg_char, content_all_text) + self.get_str_by_reg(reg_text_main, content_all_text)
        return content

    def __get_library(self):
        name = self.__get_name()
        passport = self.__get_passport()
        img = self.__get_img_url()
        content = self.__get_content()
        library = Library(name, passport, img, content)
        return library


if __name__ == "__main__":
    url = 'https://www.culture.ru/institutes/17558/politekhnicheskaya-biblioteka'
    par = ParserLibraryPage(url)
    lib = par.parse()
    print(lib.get_row_for_pandas(1))

