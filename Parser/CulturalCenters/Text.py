import requests
import re


class Text:
    def __init__(self, url):
        self.text = requests.get(url).text

    def findall(self, regular):
        return re.findall(regular, self.text)

    def get_end_search(self,reg):
        res = re.search(reg, self.text)
        idx_start, idx_end = res.start(), res.end()
        return self.text[idx_end:]

    def get_str_by_reg(self,reg):
        strs = re.findall(reg, self.text)
        str_res = " ".join(strs)
        return str_res


    def get_between(self,reg):
        res = re.search(reg, self.text)
        idx_start, idx_end = res.start(), res.end()
        return self.text[idx_start:idx_end]
