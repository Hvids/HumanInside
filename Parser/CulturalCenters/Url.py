class Url:
    @staticmethod
    def make_urls_with_postfix(url_start, postfix, range_postfix):
        start, end = tuple(range_postfix)
        urls = [f'{url_start}{postfix}{i}' for i in range(start, end)]
        return urls

    @staticmethod
    def make_urls_with_site(site, urls):
        new_urls = [site + url for url in urls]
        return  new_urls

