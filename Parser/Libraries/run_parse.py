import sys

sys.path.append('../')
sys.path.append('./')

from ParserLibrariesListPage import ParserLibrariesListPage

from Libraries import Libraries

if __name__ == '__main__':
    path_pd = '../../data/csv/libraries.csv'
    path_img = '../../data/img/libraries/'
    url_libraries_one_page = 'https://www.culture.ru/literature/libraries/location-moskva'
    site = 'https://www.culture.ru'
    url_after_one = ('https://www.culture.ru/literature/libraries/location-moskva?page=', '&limit=16&sort=-views')
    range_page = (2, 30)

    parser_list_library = ParserLibrariesListPage.create_with_generagte(site, url_libraries_one_page, url_after_one,
                                                                        range_page)
    print("make list links")
    urls_library = parser_list_library.get_urls_library()

    libraries = Libraries.parse_urls(urls_library)
    libraries.save(path_pd, path_img)
