import sys

sys.path.append('../')
import re
import requests

from Url import Url
from Text import Text
from CulturalCenter import CulturalCenters, CulturalCenter
from Event import Event, Events
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

    def parse(self, reg, text):
        name = text.get_str_by_reg(reg)
        return name


class ParserContent:
    def parse_cultural_center(self, reg, text):
        content = text.get_str_by_reg(reg)
        reg = '<span>|</span>'
        content = Parser.delete_by_reg(reg, content)
        return content

    def parser_event(self, reg, text):
        content_sub = text.get_str_by_reg(reg)
        reg = r'<p>(.*?)</p>'
        content = Parser.get_str_by_reg(reg, content_sub)
        reg = '<span>|</span>'
        content = Parser.delete_by_reg(reg, content)
        return content


class ParserPassport:

    def __get_geo_by_adress(self, adress):
        gm = 'https://www.google.com/maps/search/' + adress
        reg = r'<meta content="https://maps.google.com/maps/api/staticmap\?center=(.*?)&amp;zoom'
        text = requests.get(gm).text
        sub_geo = re.findall(reg, text)
        if len(sub_geo) > 0:
            sub_geo = sub_geo[0]
            reg_split = r'%2C'
            lat, long = tuple(re.split(reg_split, sub_geo))
            return lat, long
        else:
            return '',''

    def __get_age(self, text):
        reg = '<h3 class="sidebar-info_key" data-reactid=".*?">Ограничение по возрасту:</h3><div class="sidebar-info_value" data-reactid=".*?"><!-- react-text: .*? -->(.*?)<!-- /react-text --><!-- react-text: .*? -->(.*?)<!--'
        age_t = re.findall(reg, text)
        age_t = re.findall(reg, text)[0] if len(age_t)>0 else ''
        age = "".join(age_t)
        return age

    def __get_passport_dict(self, regs, text):
        passport = {}
        for key in regs.keys():
            passport[key] = Parser.get_str_by_reg(regs[key], text)
        return passport

    def parse_event(self, reg, text):
        sub_pass = text.get_str_by_reg(reg)
        regs = {
            'town': '<h3 class="sidebar-info_key" data-reactid=".*?">Город:</h3><div class="sidebar-info_value" data-reactid=".*?"><div data-reactid=".*?"><!-- react-text: .*? -->(.*?)<!--',
            'price': r'data-reactid=".*?">Цены на билеты:</h3><div class="sidebar-info_value" data-reactid=".*?">(.*?) руб',
        }
        passport = self.__get_passport_dict(regs, sub_pass)
        passport['age'] = self.__get_age(sub_pass)
        reg_site_buy = '<li class="sidebar-info_list-item sidebar-info_list-item__overflowed" data-reactid=".*?"><a href="(.*?)" title'
        passport['site_buy'] = text.get_str_by_reg(reg_site_buy)
        reg_date = '<button type="button" class="inline-datepicker_button button button__clean" data-reactid=".*?"><!-- react-text: .*? -->(.*?)<!--'
        passport['date'] = text.get_str_by_reg(reg_date)
        return passport

    def parse_cultural_center(self, reg, text):
        sub_content = text.get_str_by_reg(reg)
        regs = {
            'adress': r'-->(.*?)<!--',
            'number': r'<a href="tel:(.*?)"',
            'email': r'<a href="mailto:(.*?)"',
            'social_netwoks': r'<div class="social-links" data-reactid=".*?"><a href="(.*?)" target="_blank noopener noreferrer" class="social-links_item" data-reactid=".*?">',
            'undegroud': r'<!-- /react-text -->  data-reactid=".*?">(.*?) data-reactid=".*?">',
        }

        passport = self.__get_passport_dict(regs, sub_content)
        passport['adress'] = re.sub(r'\s+', ' ', passport['adress'])
        passport['latitude'], passport['logitute'] = self.__get_geo_by_adress(passport['adress'])
        reg_off_site = r'<div class="sidebar-info_row" data-reactid=".*?"><h3 class="sidebar-info_key" data-reactid=".*?">Официальный сайт:</h3><div class="sidebar-info_value" data-reactid=".*?"><a href="(.*?)"'
        passport['offical_site'] = text.get_str_by_reg(reg_off_site)
        return passport


class ParserEvent:
    def __init__(self, site, url):
        self.site = site
        self.url = url
        self.text = Text(url)

    @property
    def __name(self):
        reg = r'<div class="entity-info_title" data-reactid=".*?">(.*?)</div>'
        parser_name = ParserName()
        name = parser_name.parse(reg, self.text)
        return name

    @property
    def __content(self):
        reg = r'<div class="content_view content_view__text" data-reactid=".*?">(.*?)</div>'
        parser_content = ParserContent()
        content = parser_content.parser_event(reg, self.text)
        return content

    @property
    def passport(self):
        reg = r'<div class="sidebar-info_row" data-reactid=".*?">(.*?)</div>'
        parser_passport = ParserPassport()
        passport = parser_passport.parse_event(reg, self.text)
        return passport

    @property
    def __img_url(self):
        reg = r'<img class="image image__clickable entity-info_image" src="(.*?)"'
        parser_img_url = ParseImgUrl(prefix=self.site)
        img_url = parser_img_url.parse(reg, self.text)
        return img_url

    def parse(self, id_cultural):
        name = self.__name
        content = self.__content
        img_url = self.__img_url
        passport = self.passport
        event = Event(id_cultural, name, content, img_url, passport)
        return event


class ParserEvents:
    def __init__(self, site, url):
        self.url = url
        self.site = site
        self.url_events = self.__make_url_events()

    def __make_url_events(self):
        text = Text(self.url)
        reg = r'<div class="content-list_item" data-reactid=".*?"><div class="content-list_item-info" data-reactid=".*?"><div class="media-preview" data-reactid=".*?"><a class="media-preview_img-wrap" href="(.*?)"'
        urls = text.findall(reg)
        urls = Url.make_urls_with_site(self.site, urls)
        return urls

    def parse(self, id_cultural):
        result_events = Events()
        for id, url in enumerate(self.url_events):
            parser_event = ParserEvent(self.site, url)
            event = parser_event.parse(id_cultural)
            print(f'ev = {event.id}  {event.name}')
            result_events.add(event)
        return result_events


class ParserCulturalCenter:
    def __init__(self, site, url):
        self.site = site
        self.url = url
        self.text = Text(url)

    @property
    def __name(self):
        reg = r'<h1 class="entity-info_title" data-reactid=".*?">(.*?)</h1>'
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
        reg_content = r'<p>(.*?)</p>'
        parser_content = ParserContent()
        content = parser_content.parse_cultural_center(reg_content, self.text)
        return content

    @property
    def __passport(self):
        reg_passport = r'<div class="sidebar-info_value"(.*?)</div>'
        parser_passport = ParserPassport()
        passport = parser_passport.parse_cultural_center(reg_passport, self.text)
        return passport

    def __parse_events(self, id_cultural):
        parser_events = ParserEvents(self.site, self.url)
        events = parser_events.parse(id_cultural)
        return events

    def parse_center(self, id) -> object:
        name = self.__name
        img_url = self.__img_url
        content = self.__content
        passport = self.__passport
        events = self.__parse_events(id)

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
            print(f'cc = {center.id} {center.name}')
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
