import sys

sys.path.append('../')
import re
import requests


from Text import Text
from CulturalCenter import CulturalCenters, CulturalCenter
from Event import Event, Events
from Parser import ParserUrls, ParserDataList, ParserData, ParserElement


class ParseImgUrl:
    def __init__(self, width=500, height=500, prefix=''):
        self.prefix = prefix
        self.width = width
        self.height = height

    def url_with_prefix(self, pre_url):
        return self.prefix + pre_url

    def set_size(self, pre_url):
        reg_format = r'\.(.*)'
        pre_format = pre_url.get_str_by_reg(reg_format)
        reg_url = '(.*?)_w'
        url = pre_url.get_str_by_reg(reg_url)
        res_pre_url = f'{url}_w{self.width}_h{self.height}.{pre_format}'
        return res_pre_url

    def parse(self, reg, text):
        pre_url = text.create_by_reg(reg)
        pre_url = self.set_size(pre_url)
        url = self.url_with_prefix(pre_url)
        return url


class ParserPassport(ParserElement):
    @staticmethod
    def get_geo_by_adress(adress):
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
            return '', ''

    @property
    def age(self):
        reg = r'<h3 class="sidebar-info_key" data-reactid=".*?">Ограничение по возрасту:</h3><div class="sidebar-info_value" data-reactid=".*?"><!-- react-text: .*? -->(.*?)<!-- /react-text --><!-- react-text: .*? -->(.*?)<!--'
        age_t = re.findall(reg, self.text.text)
        age_t = age_t[0] if len(age_t) > 0 else ''
        age = "".join(age_t)
        return age

    def parse_event(self, reg):
        sub_pass = self.text.create_by_reg(reg)
        regs_sub = {
            'town': '<h3 class="sidebar-info_key" data-reactid=".*?">Город:</h3><div class="sidebar-info_value" data-reactid=".*?"><div data-reactid=".*?"><!-- react-text: .*? -->(.*?)<!--',
            'price': r'data-reactid=".*?">Цены на билеты:</h3><div class="sidebar-info_value" data-reactid=".*?">(.*?) руб',
        }
        regs = {
            'name': r'<div class="entity-info_title" data-reactid=".*?">(.*?)</div>',
            'site_buy': '<li class="sidebar-info_list-item sidebar-info_list-item__overflowed" data-reactid=".*?"><a href="(.*?)" title',
            'date': '<button type="button" class="inline-datepicker_button button button__clean" data-reactid=".*?"><!-- react-text: .*? -->(.*?)<!--'
        }

        passport_sub = sub_pass.parse_passport(regs_sub)
        passport = self.text.parse_passport(regs)
        passport = dict(passport,**passport_sub)
        passport['age'] = self.age
        return passport

    def parse_cultural_center(self, reg):
        sub_content = self.text.create_by_reg(reg)
        regs_sub = {
            'adress': r'-->(.*?)<!--',
            'number': r'<a href="tel:(.*?)"',
            'email': r'<a href="mailto:(.*?)"',
            'social_netwoks': r'<div class="social-links" data-reactid=".*?"><a href="(.*?)" target="_blank noopener noreferrer" class="social-links_item" data-reactid=".*?">',

        }
        regs = {
            'name': r'<h1 class="entity-info_title" data-reactid=".*?">(.*?)</h1>',
            'offical_site': r'<div class="sidebar-info_row" data-reactid=".*?"><h3 class="sidebar-info_key" data-reactid=".*?">Официальный сайт:</h3><div class="sidebar-info_value" data-reactid=".*?"><a href="(.*?)"',
            'undegroud': r'<div class="sidebar-info_row" data-reactid=".*?"><h3 class="sidebar-info_key" data-reactid=".*?">Метро:</h3><div class="sidebar-info_value" data-reactid=".*?">(.*?)</div></div>',
        }
        passsport = self.text.parse_passport(regs)
        passport_sub = sub_content.parse_passport(regs_sub)
        passport = dict(passsport,**passport_sub)

        passport['adress'] = re.sub(r'\s+', ' ', passport['adress'])
        passport['latitude'], passport['logitute'] = self.get_geo_by_adress(passport['adress'])

        return passport


class ParserEvent(ParserData):
    name = 'Parser Event'
    def __init__(self, site, url):
        self.site = site
        self.url = url
        self.text = Text.create_by_url(url)

    @property
    def content(self):
        reg = r'<div class="content_view content_view__text" data-reactid=".*?">(.*?)</div>'
        content = self.parse_content(reg)
        return content

    @property
    def passport(self):
        reg = r'<div class="sidebar-info_row" data-reactid=".*?">(.*?)</div>'
        parser_passport = ParserPassport(self.site, self.text)
        passport = parser_passport.parse_event(reg)
        return passport

    @property
    def img_url(self):
        reg = r'<img class="image image__clickable entity-info_image" src="(.*?)"'
        parser_img_url = ParseImgUrl(prefix=self.site)
        img_url = parser_img_url.parse(reg, self.text)
        return img_url

    def parse(self, id_cultural):
        passport = self.passport
        passport['img_url'] = self.img_url
        passport['content'] = self.content
        event = Event(id_cultural, passport)
        return event


class ParserEvents(ParserDataList):
    name = 'Parser Events'
    def parse_events(self, id_cultural):
        parser_event_obj = ParserEvent
        events_obj = Events
        events = self.parse(events_obj, parser_event_obj, id_pred=id_cultural, proc = False)
        return events


class ParserUrlsEvent(ParserUrls):
    name = 'Parser Urls Event'

    @property
    def urls(self):
        reg = r'<div class="content-list_item" data-reactid=".*?"><div class="content-list_item-info" data-reactid=".*?"><div class="media-preview" data-reactid=".*?"><a class="media-preview_img-wrap" href="(.*?)"'
        text = Text.create_by_url(self.url.url)
        urls = text.findall(reg)
        urls = self.url.concat_site_with_bodies(urls)
        return urls


class ParserCulturalCenter(ParserData):
    name = 'ParserCulturalCenter'
    @property
    def img_url(self):
        reg = r'<img class="image image__clickable entity-info_image" src="(.*?)"'
        img_url = self.parser_img(reg)
        return img_url

    @property
    def content(self):
        reg = r'.*'
        content = self.parse_content(reg)
        return content

    def parse_events(self, id_cultural):
        parser_urls = ParserUrlsEvent(self.site, self.url)
        urls = parser_urls.urls
        parser_events = ParserEvents(self.site, urls)
        events = parser_events.parse_events(id_cultural)
        return events

    @property
    def passport(self):
        reg = r'<div class="sidebar-info_value"(.*?)</div>'
        parser_passport = ParserPassport(self.site, self.text)
        passport = parser_passport.parse_cultural_center(reg)
        return passport

    def parse(self, id):
        passport = self.passport
        passport['img_url'] = self.img_url
        passport['content'] = self.content

        events = self.parse_events(id)

        return CulturalCenter(passport, events)


class ParserCulturalCenters(ParserDataList):
    name = 'Parser Cultural Centers'
    @property
    def cultural_centers(self):
        cultural_centers_obj = CulturalCenters
        parser_cultural_center_obj = ParserCulturalCenter
        books = self.parse(cultural_centers_obj, parser_cultural_center_obj)
        return books


class ParserUrlsCulturalCenters(ParserUrls):
    name = 'Parser Urls Cultural Centers'

    def get_urls(self, range_postfix):
        reg = r'<a class="media-card media-card__height__medium media-card__width__small media-card__base-color" href="(.*?)" data-reactid="'
        ursl = self.parse(reg, range_postfix)
        return ursl
