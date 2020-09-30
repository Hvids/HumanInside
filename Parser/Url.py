class Url:
    def __init__(self, prefix, body, postfix=''):
        self.prefix = prefix
        self.postfix = postfix
        self.body = body


    def link(self, value):
        return f'{self.prefix}{self.body}{self.postfix}{value}'

    def concat_prefix_wiht_url(self,urls):
        return  Url.make_urls_with_site(self.prefix,urls)

    @staticmethod
    def make_urls_with_postfix(url_start, postfix, range_postfix):
        start, end = tuple(range_postfix)
        urls = [f'{url_start}{postfix}{i}' for i in range(start, end)]
        return urls

    @staticmethod
    def make_urls_with_site(site, urls):
        new_urls = [site + url for url in urls]
        return new_urls
