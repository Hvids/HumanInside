import requests
import re


class ParserLibrariesListPage:
    def __init__(self, site, urls):
        self.site = site
        self.urls = urls

    def __get_urls_library_page(self, url):
        text = requests.get(url).text
        regular_sub_text = r'<div class="entity-cards grid-1-noSpaceTop_notebook-4_tablet-medium-3_mobile-large-2">(.*)</div>'
        result_sub_text = re.search(regular_sub_text, text)
        idx_start, idx_end = result_sub_text.start(), result_sub_text.end()
        text = text[idx_start:idx_end]
        regular_list_urls = r'<div class="entity-card-v2_body"><a href="(.*?)"'
        urls = re.findall(regular_list_urls, text)
        urls = [self.site + url for url in urls]
        return urls

    def get_urls_library(self):
        urls_library_page = []
        for url_page_list in self.urls:
            urls_page_list = self.__get_urls_library_page(url_page_list)
            urls_library_page += urls_page_list
        return urls_library_page

    @classmethod
    def create_with_generagte(
            cls,
            site,
            url_libraries_one_page,
            url_after_one,
            range_page_after_one
    ):
        urls = cls.generate_urls_parse(
            url_libraries_one_page,
            url_after_one,
            range_page_after_one
        )
        return cls(site, urls)

    @staticmethod
    def generate_urls_parse(
            url_libraries_one_page,
            url_after_one,
            range_page_after_one

    ):
        url_after_one_libraries_left, url_after_one_libraries_rigth = url_after_one
        start_after_one, end_after_one = range_page_after_one[0], range_page_after_one[1] + 1
        urls = [url_libraries_one_page] \
               + \
               [
                   url_after_one_libraries_left + str(i) + url_after_one_libraries_rigth
                   for i in range(start_after_one, end_after_one)
               ]
        return urls


if __name__ == '__main__':
    url_libraries = 'https://www.culture.ru/literature/libraries/location-moskva'
    site = 'https://www.culture.ru'
    url_after_one = ('https://www.culture.ru/literature/libraries/location-moskva?page=', '&limit=16&sort=-views')
    range_page = (2, 30)
    parser = ParserLibrariesListPage.create_with_generagte(site, url_libraries, url_after_one, range_page)
    print(parser.get_urls_library())
