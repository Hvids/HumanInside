import re


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
    def delete_by_reg(reg,text):
        strs = re.split(reg,text)
        str_res = "".join(strs)
        return str_res