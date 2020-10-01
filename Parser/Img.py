from PIL import Image
import requests
from io import BytesIO
from tqdm import tqdm


class Img:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def save(self, path_img):
        try:
            response = requests.get(self.url)
            img = Image.open(BytesIO(response.content))
            img.convert('RGB').save(path_img + str(self.name) + '.png', "PNG", optimize=True)
        except:
            return None


class SaverImgs:
    def __init__(self, columns_id, columns_url):
        self.columns_id = columns_id
        self.columns_url = columns_url

    @property
    def size(self):
        return len(self.columns_url)

    def save(self, path):
        for i in tqdm(range(self.size), desc='Save Imgs'):
            id, url = self.columns_id[i], self.columns_url[i]
            img = Img(id, url)
            img.save(path)
        return None
