from Library import Library
from ParserLibraryPage import ParserLibraryPage
import pandas as pd


class Libraries:
    def __init__(self, libraries=[]):
        self.libraries = libraries

    @property
    def attrs_name(self):
        return self.libraries[0].attrs_name

    def save(self, path_pd, path_img, verobose=1):
        if verobose == 1:
            print('save')
        attrs_name = self.attrs_name
        data = pd.DataFrame(columns=attrs_name)
        for id, lib in enumerate(self.libraries):
            lib.save_img(id, path_img)
            row = lib.get_row_for_pandas(id)
            data = data.append(row, ignore_index=True)
        data.to_csv(path_pd, index=False)

    @classmethod
    def parse_urls(cls, urls, verbose=1):
        libs = []
        if verbose == 1:
            print("parse library")
        for i, url in enumerate(urls):
            parser = ParserLibraryPage(url)
            lib = parser.parse()
            if verbose == 1:
                print(lib.name)

            libs.append(lib)
        return cls(libraries=libs)
