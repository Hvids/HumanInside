from PIL import Image
import requests
from io import BytesIO

class Img:
    def __init__(self,name, url):
        self.name = name
        self.url = url


    def save_img(self, path_img):
        try:
            response = requests.get(self.url)
            img = Image.open(BytesIO(response.content))
            img.convert('RGB').save(path_img + str(self.name)+'.png', "PNG", optimize=True)
        except OSError:
            print(f'non image download {self.name}')
            return  None

class SaverImgs:
    def __init__(self, colums_id, colums_url):
        self.colums_id = colums_id
        self.colums_url = colums_url

    def save(self, path):
        for id, url in zip(self.colums_id, self.colums_url):
            img = Img(id,url)
            img.save_img(path)
