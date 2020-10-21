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


class FinderBook(FinderBase):
    def __init__(self, loader_type=FilteringBooks.load_model(), get_type=Book):
        super(FinderBook, self).__init__(loader_type, get_type)


class FinderEvent(FinderBase):
    def __init__(self, loader_type=FilteringEvents.load_model(), get_type=Event):
        super(FinderEvent, self).__init__(loader_type, get_type)


class FinderCenter(FinderBase):
    def __init__(self, loader_type=FilteringCulturalCenters.load_model(), get_type=CultureCenter):
        super(FinderCenter, self).__init__(loader_type, get_type)
