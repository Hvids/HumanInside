import sys

sys.path.append('../')
import re
import requests

from Url import Url
from Text import Text
from CulturalCenter import CulturalCenters, CulturalCenter

from Parser import Parser


class ParseImgUrl:
    def __init__(self, width=500, height=500, prefix=''):
        self.prefix = prefix
        self.width = width
        self.height = height

    def __url_with_prefix(self, pre_url):
        return self.prefix + pre_url

    def __set_size(self, pre_url):
        reg_format = r'\.(.*)'
        pre_format = Parser.get_str_by_reg(reg_format, pre_url)
        reg_url = '(.*?)_w'
        url = Parser.get_str_by_reg(reg_url, pre_url)
        res_pre_url = f'{url}_w{self.width}_h{self.height}.{pre_format}'
        return res_pre_url

    def parse(self, reg, text):
        pre_url = text.get_str_by_reg(reg)
        pre_url = self.__set_size(pre_url)
        url = self.__url_with_prefix(pre_url)
        return url


class ParserName:
    def __init__(self):
        pass

    def parse(self, reg, text):
        sub_name = text.get_str_by_reg(reg)
        reg_name = r'>(.*)'
        name = Parser.get_str_by_reg(reg_name, sub_name)
        return name


class ParserContent:
    def __init__(self):
        pass

    def parse(self, reg, text):
        sub_content = text.get_str_by_reg(reg)
        reg = r'<p>(.*?)</p>'
        sub_content = Parser.get_str_by_reg(reg,sub_content)
        reg_split = r'<span>|</span>'
        content = Parser.delete_by_reg(reg_split, sub_content)
        return content


class ParserPassport:

    def __get_geo_by_adress(self, adress):
        gm = 'https://www.google.com/maps/search/' + adress
        reg = r'<meta content="https://maps.google.com/maps/api/staticmap\?center=(.*?)&amp;zoom'
        text = requests.get(gm).text
        sub_geo = re.findall(reg, text)[0]
        reg_split = '%2C'
        lat, long = tuple(re.split(reg_split, sub_geo))
        return lat, long

    def __get_passport_dict(self, regs, text):
        passport = {}
        for key in regs.keys():
            passport[key] = Parser.get_str_by_reg(regs[key], text)
        return passport

    def parse(self, reg, text):
        sub_content = text.get_str_by_reg(reg)
        regs = {
            'adress': r'-->(.*?)<!--',
            'number': r'<a href="tel:(.*?)"',
            'email': r'<a href="mailto:(.*?)"',
            'social_netwoks': r'<div class="social-links" data-reactid=".*?"><a href="(.*?)" target="_blank noopener noreferrer" class="social-links_item" data-reactid=".*?">',
            'undegroud': r'<!-- /react-text -->  data-reactid=".*?">(.*?) data-reactid=".*?">',
        }

        passport = self.__get_passport_dict(regs, sub_content)
        passport['latitude'], passport['logitute'] = self.__get_geo_by_adress(passport['adress'])
        reg_off_site = r'<div class="sidebar-info_row" data-reactid=".*?"><h3 class="sidebar-info_key" data-reactid="774">Официальный сайт:</h3><div class="sidebar-info_value" data-reactid="775"><a href="(.*?)"'
        passport['offical_site'] = text.get_str_by_reg(reg_off_site)
        return passport


class ParserCulturalCenter:
    def __init__(self, site, url):
        self.site = site
        self.url = url
        self.text = Text(url)

    @property
    def __name(self):
        reg = r'<h1 class="entity-info_title"(.*?)</h1>'
        parser_name = ParserName()
        name = parser_name.parse(reg, self.text)
        return name
    @property
    def __img_url(self):
        reg = r'<img class="image image__clickable entity-info_image" src="(.*?)"'
        parser_img_url = ParseImgUrl(prefix=self.site)
        url = parser_img_url.parse(reg, self.text)
        return url

    @property
    def __content(self):
        reg_content = r'<div class="content_view content_view__text"(.*?)</div></div></div>'
        parser_content = ParserContent()
        content = parser_content.parse(reg_content, self.text)
        return content

    @property
    def __passport(self):
        reg_passport = r'<div class="sidebar-info_value"(.*?)</div>'
        parser_passport = ParserPassport()
        passport = parser_passport.parse(reg_passport, self.text)
        return passport

    def __events(self):
        return None

    def parse_center(self, id):
        name = self.__name
        img_url = self.__img_url
        content = self.__content
        passport = self.__passport
        events = self.__events
        return CulturalCenter(id, name, passport, content, img_url, events)


class ParserCulturalCenters:
    def __init__(self, site, urls):
        self.site = site
        self.urls = urls

    @property
    def cultural_centers(self):
        centers = CulturalCenters()
        for id, url in enumerate(self.urls):
            parser_cultural_center = ParserCulturalCenter(self.site, url)
            center = parser_cultural_center.parse_center(id)
            centers.add(center)
        return centers


class ParserUrlsCulturalCenters:
    def __init__(self, site, url_start_page, postfix, range_postfix):
        self.site = site
        self.url_start_page = url_start_page
        self.postfix = postfix
        self.range_postfix = range_postfix
        self.urls_parse = Url.make_urls_with_postfix(url_start_page, postfix, range_postfix)

    @property
    def urls(self):
        result = []
        urls_img = []
        regular_urls = r'<a class="media-card media-card__height__medium media-card__width__small media-card__base-color" href="(.*?)" data-reactid="'

        for url in self.urls_parse:
            text = Text(url)
            urls_cultural_centers_page = text.findall(regular_urls)
            urls_with_site = Url.make_urls_with_site(self.site, urls_cultural_centers_page)
            result.extend(urls_with_site)

        return result
