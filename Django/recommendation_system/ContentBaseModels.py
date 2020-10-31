from polls.models import *
import json
from .Maker import *
from .names import *
from .paths import *


class ContentBase:
    def __init__(self, SeceltObject, data, id_name, count_last=5):
        self.count_last = count_last
        self.data = data
        self.SelectObject = SeceltObject
        self.id_name = id_name

    def get_list(self, tuple_list):
        return [t[0] for t in tuple_list]

    def recommend(self, id_user):
        objects_read_user = self.SelectObject.objects.filter(id_user=id_user).order_by('-id').values_list(self.id_name)
        objects_read_user = self.get_list(objects_read_user)[:self.count_last]
        result = []
        for object_read_user in objects_read_user:
            best = self.data[str(object_read_user)]
            for i in best:
                if i not in objects_read_user and i not in result:
                    result.append(i)
                    break

        return result

    @staticmethod
    def load_json(name, path):
        with open(f"{path}{name}.json", "r") as write_file:
            f = json.load(write_file)
        return f

    def update_with_makers(self, maker_df, maker_json):
        maker_df.make(fit=True)
        maker_json.make()


class ContentBaseBooks(ContentBase):
    @classmethod
    def load(cls, name_json=SIMILAR_BOOKS, path_json=PATH_DATA_JSON, count_last=5):
        data = cls.load_json(name_json, path_json)
        return cls(LastBook, data, 'id_book', count_last=count_last)

    def update(self):
        maker_preprocessing_data = MakerMatrixPreprocessingBooks()
        maker_similar_json = MakerSimilarJSONBooks()
        self.update_with_makers(maker_preprocessing_data, maker_similar_json)
        return ContentBaseBooks.load()


class ContentBaseEvents(ContentBase):
    @classmethod
    def load(cls, name_json=SIMILAR_EVENTS, path_json=PATH_DATA_JSON, count_last=5):
        data = cls.load_json(name_json, path_json)
        return cls(LastEvent, data, 'id_event', count_last=count_last)

    def update(self):
        maker_preprocessing_data = MakerMatrixPreprocessingEvents()
        maker_similar_json = MakerSimilarJSONEvents()
        self.update_with_makers(maker_preprocessing_data, maker_similar_json)
        return ContentBaseEvents.load()

class ContentBaseSections(ContentBase):
    @classmethod
    def load(cls, name_json=SIMILAR_SECTIONS, path_json=PATH_DATA_JSON, count_last=5):
        data = cls.load_json(name_json, path_json)
        return cls(LastSection, data, 'id_section', count_last=count_last)

    def update(self):
        maker_preprocessing_data = MakerMatrixPreprocessingSections()
        maker_similar_json = MakerSimilarJSONSections()
        self.update_with_makers(maker_preprocessing_data, maker_similar_json)
        return ContentBaseEvents.load()

# from recommendation_system.ContentBaseModels import ContentBaseBooks, ContentBaseEvents, ContentBaseCulturalCenters; cb = ContentBaseBooks();cb.update()
