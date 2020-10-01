class Url:
    def __init__(self, site, url, postfix=''):
        self.site = site
        self.url = url
        self.postfix = postfix

    def link(self, value):
        return f'{self.url}{self.postfix}{value}'

    def concat_site_with_bodies(self, urls):
        return Url.make_urls_with_site(self.site, urls)

    @staticmethod
    def make_urls_with_postfix(url_start, postfix, range_postfix):
        start, end = tuple(range_postfix)
        urls = [f'{url_start}{postfix}{i}' for i in range(start, end)]
        return urls

    @staticmethod
    def make_urls_with_site(site, urls):
        new_urls = [site + url for url in urls]
        return new_urls
