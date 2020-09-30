from PIL import Image
import requests
from io import BytesIO


class Img:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def save(self, path_img):
        print(f'{self.url}')
        try:
            response = requests.get(self.url)
            img = Image.open(BytesIO(response.content))
            img.convert('RGB').save(path_img + str(self.name) + '.png', "PNG", optimize=True)
        except:
            print(f'non image download {self.name}')
            return None


class SaverImgs:
    def __init__(self, columns_id, columns_url):
        self.columns_id = columns_id
        self.columns_url = columns_url

    def save(self, path):
        for id, url in zip(self.columns_id, self.columns_url):
            img = Img(id, url)
            img.save(path)
        return None
