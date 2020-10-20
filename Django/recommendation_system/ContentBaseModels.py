from polls.models import *
import json
from .Updater import UpdaterJson
from .management.commands.Maker import MakerSimilarJson, MakerMatrixBooks, MakerMatrixEvents, MakerMatrixCulturalCenters, MakerMatrixTemp

class ContentBase:
    def load(self, name, path):
        with open(f"{path}{name}", "r") as write_file:
            f = json.load(write_file)
        return f

    def update_json(self, updater):
        updater.update()


class ContentBaseBooks(ContentBase):
    def __init__(self, k=5):
        self.Temp = LastBook
        self.similar = self.load('books.json', './recommendation_system/data/json/')
        self.k = k

    def get_list(self, tuple_list):
        return [t[0] for t in tuple_list]

    def recommend(self, id_user):
        books_read_user = self.Temp.objects.filter(id_user=id_user).order_by('-id').values_list('id_book')
        books_read_user = self.get_list(books_read_user)[:self.k]
        result = []
        for book_read_user in books_read_user:
            best = self.similar[str(book_read_user)]
            for i in best:
                if i not in books_read_user and i not in result:
                    result.append(i)
                    break

        return result

    def update(self):
        updater = UpdaterJson(
            name='books',
            select_columns=['id', 'author', 'pages', 'rating', 'language', 'content'],
            maker_temp = MakerMatrixTemp(Book),
            maker_df=MakerMatrixBooks(),
            maker_json=MakerSimilarJson()
        )
        self.update_json(updater)


class ContentBaseEvents(ContentBase):
    def __init__(self, k=5):
        self.Temp = LastEvent
        self.similar = self.load('events.json', './recommendation_system/data/json/')
        self.k = k

    def get_list(self, tuple_list):
        return [t[0] for t in tuple_list]

    def recommend(self, id_user):
        events_visit_user = self.Temp.objects.filter(id_user=id_user).order_by('-id').values_list('id_event')
        events_visit_user = self.get_list(events_visit_user)[:self.k]
        result = []
        for event_visit_user in events_visit_user:
            best = self.similar[str(event_visit_user)]
            for i in best:
                if i not in events_visit_user and i not in result:
                    result.append(i)
                    break

        return result

    def update(self):
        updater = UpdaterJson(
            name='events',
            select_columns= ['id', 'town', 'price', 'age_rate', 'content'],
            maker_temp = MakerMatrixTemp(Event),
            maker_df=MakerMatrixEvents(),
            maker_json=MakerSimilarJson()
        )
        self.update_json(updater)


class ContentBaseCulturalCenters(ContentBase):
    def __init__(self, k=5):
        self.Temp = LastCenter
        self.similar = self.load('cultural_centers.json', './recommendation_system/data/json/')
        self.k = k

    def get_list(self, tuple_list):
        return [t[0] for t in tuple_list]

    def recommend(self, id_user):
        centers_visit_user = self.Temp.objects.filter(id_user=id_user).order_by('-id').values_list('id_center')
        centers_visit_user = self.get_list(centers_visit_user)[:self.k]
        result = []
        for center_visit_user in centers_visit_user:
            best = self.similar[str(center_visit_user)]
            for i in best:
                if i not in centers_visit_user and i not in result:
                    result.append(i)
                    break

        return result

    def update(self):
        updater = UpdaterJson(
            name='cultural_centers',
            select_columns= ['id', 'underground', 'latitude', 'longitude', 'content'],
            maker_temp = MakerMatrixTemp(CultureCenter),
            maker_df=MakerMatrixCulturalCenters(),
            maker_json=MakerSimilarJson(),
        )
        self.update_json(updater)
# from recommendation_system.ContentBaseModels import ContentBaseBooks, ContentBaseEvents, ContentBaseCulturalCenters; cb = ContentBaseBooks();cb.update()

