from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .functions import *
from recommendation_system.FilteringModels import *


class FinderBase:
    def __init__(self, loader_type, get_type):
        self.loader_type = loader_type
        self.get_type = get_type

    def find(self, request, id_user):
        loader = self.loader_type
        recommendation_id = loader.recommend(id_user=id_user)
        recommendation_list = []
        for idx in recommendation_id:
            recommendation_list.append(self.get_type.objects.get(id=idx))
        return render(request, 'polls/recommendation.html', {'recommendation_list': recommendation_list})

    def findAll(self, request, id_user):
        allInOne = []

        for loader, type_ in zip(self.loader_type, self.get_type):
            rec_id = loader.recommend(id_user=id_user)
            partOf = []
            for idx in rec_id:
                partOf.append(type_.objects.get(id=idx))
            allInOne.append(partOf)

        dictAllInOne = dict()
        dictAllInOne['ID_user'] = id_user
        dictAllInOne['Books'] = allInOne[0]
        dictAllInOne['Events'] = allInOne[1]
        dictAllInOne['Centers'] = allInOne[2]
        return render(request, 'polls/home.html', dictAllInOne)


class FinderBook(FinderBase):
    def __init__(self, loader_type=FilteringBooks.load_model(), get_type=Book):
        super(FinderBook, self).__init__(loader_type, get_type)


class FinderEvent(FinderBase):
    def __init__(self, loader_type=FilteringEvents.load_model(), get_type=Event):
        super(FinderEvent, self).__init__(loader_type, get_type)


class FinderCenter(FinderBase):
    def __init__(self, loader_type=FilteringCulturalCenters.load_model(), get_type=CultureCenter):
        super(FinderCenter, self).__init__(loader_type, get_type)


class FindAll(FinderBase):
    def __init__(self, loader_type=[FilteringBooks.load_model(), FilteringEvents.load_model(),
                                    FilteringCulturalCenters.load_model()], get_type=[Book, Event, CultureCenter]):
        super(FindAll, self).__init__(loader_type, get_type)
