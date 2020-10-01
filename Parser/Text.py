import requests
import re


class ParserText:
    def parse_passport(self, regs):
        passport = {}
        for key in regs.keys():
            passport[key] = self.get_str_by_reg(regs[key])
        return passport

class Text(ParserText):
    def __init__(self, text):
        self.text = text

    def create_by_reg(self, reg):
        text = self.get_str_by_reg(reg)
        return Text(text)

    def delete_by_reg(self, reg):
        strs = re.split(reg, self.text)
        str_res = "".join(strs)
        return str_res

    @classmethod
    def create_by_url(cls, url):
        text = requests.get(url).text
        return cls(text)

    def findall(self, regular):
        return re.findall(regular, self.text)

    def get_end_search(self, reg):
        res = re.search(reg, self.text)
        idx_start, idx_end = res.start(), res.end()
        return self.text[idx_end:]

    def get_str_by_reg(self, reg):
        strs = re.findall(reg, self.text)
        str_res = " ".join(strs)
        return str_res

    def get_between(self, reg):
        res = re.search(reg, self.text)
        idx_start, idx_end = res.start(), res.end()
        return self.text[idx_start:idx_end]

