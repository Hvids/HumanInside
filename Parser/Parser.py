import re
from tqdm import tqdm
from Url import Url
from Text import ParserText, Text
import time


class ParserElement:
    def __init__(self, site, text):
        self.site = site
        self.text = text


class ParserSocialNetwork(ParserElement):
    def parse(self, reg):
        soc_net = self.text.create_by_reg(reg)
        reg = r'<a href="(.*?)"'
        soc_net = soc_net.get_str_by_reg(reg)
        return soc_net


class ParserImgUrl(ParserElement):
    def parse(self, reg):
        img_url = self.text.get_str_by_reg(reg)
        img_url = self.site + img_url
        return img_url


class ParserContent(ParserElement):
    def parse(self, reg):
        content = self.text.create_by_reg(reg)
        reg = r'<p>(.*?)</p>'
        content = content.create_by_reg(reg)
        reg = '<span.*?>|</span>|<a.*?>.*?</a>|<strong.*?>|</strong><br/>'
        content = content.delete_by_reg(reg)
        return content


class ParserData(ParserText):
    def __init__(self, site, url):
        self.url = url
        self.site = site
        self.text = Text.create_by_url(url)

    def parse_social_networks(self, reg):
        parser_social_network = ParserSocialNetwork(self.site, self.text)
        soc_net = parser_social_network.parse(reg)
        return soc_net

    def parser_img(self, reg):
        parer_img = ParserImgUrl(self.site, self.text)
        img_url = parer_img.parse(reg)
        return img_url

    def parse_content(self, reg):
        parser_content = ParserContent(self.site, self.text)
        content = parser_content.parse(reg)
        return content


class ParserDataList:
    def __init__(self, site, urls):
        self.urls = urls
        self.site = site

    def parse(self, data_list_obj, parse_obj, id_pred=0, proc=True):
        data_list = data_list_obj()
        if proc == True:
            for id in tqdm(range(len(self.urls)), desc=f'{self.name}'):
                url = self.urls[id]
                parser = parse_obj(self.site, url)
                data = parser.parse(id_pred)
                data_list.add(data)
        else:
            for id in range(len(self.urls)):
                url = self.urls[id]
                parser = parse_obj(self.site, url)
                data = parser.parse(id_pred)
                data_list.add(data)

        return data_list



class ParserUrls:
    name = 'ParseUrls'

    def __init__(self, site, url, postfix=''):
        self.url = Url(site, url, postfix)

    def parse(self, reg, range_postfix):
        bodies = []
        start, end = tuple(range_postfix)
        for i in tqdm(range(start, end), desc=f'{self.name}'):
            url = self.url.link(i)
            text = Text.create_by_url(url)
            bodies_sub = text.findall(reg)
            bodies.extend(bodies_sub)

        urls = self.url.concat_site_with_bodies(bodies)
        return urls
