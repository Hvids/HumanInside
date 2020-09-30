import re

from Url import Url
from Text import Text


class ParserData:
    def __init__(self, site,url):
        self.url = url
        self.site = site
        self.text = Text(url)


class ParserDataList:
    def __init__(self, site,urls):
        self.urls = urls
        self.site = site


class ParserUrls:
    def __init__(self, prefix, body, postfix):
        self.url = Url(prefix, body, postfix)

    def parse(self, reg, range_postfix):
        urls = []
        start, end = tuple(range_postfix)
        for i in range(start, end):
            url = self.url.link(i)
            text = Text(url)
            urls_sub = text.findall(reg)
            urls.extend(urls_sub)
        urls = self.url.concat_prefix_wiht_url(urls)
        return urls


class Parser:

    @staticmethod
    def get_end_search(reg, text):
        res = re.search(reg, text)
        idx_start, idx_end = res.start(), res.end()
        return text[idx_end:]

    @staticmethod
    def get_str_by_reg(reg, text):
        strs = re.findall(reg, text)
        str_res = " ".join(strs)
        return str_res

    @staticmethod
    def get_between(reg, text):
        res = re.search(reg, text)
        idx_start, idx_end = res.start(), res.end()
        return text[idx_start:idx_end]

    @staticmethod
    def delete_by_reg(reg, text):
        strs = re.split(reg, text)
        str_res = "".join(strs)
        return str_res
