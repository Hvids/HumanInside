from copy import deepcopy


class CulturalCenter:
    def __init__(self, id, name, passport, content, img_url, events):
        self.id = id
        self.name = name
        self.passport = passport
        self.img_url = img_url
        self.events = events
        self.content = content

    @property
    def row(self):
        row = deepcopy(self.passport)
        row['id'] = self.id
        row['name'] = self.name
        row['img_url'] = self.img_url
        row['content'] = self.content
        return row

    def __str__(self):
        return str(self.row)


class CulturalCenters:
    def __init__(self, ceneters=[]):
        self.centers = ceneters
