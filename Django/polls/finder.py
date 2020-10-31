from django.shortcuts import render
from django.http import HttpResponse
from .models import *
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
        return render(request, 'polls/home.html', dictAllInOne)


class FinderBook(FinderBase):
    def __init__(self, loader_type=FilteringBooks.load_model(), get_type=Book):
        super(FinderBook, self).__init__(loader_type, get_type)


class FinderEvent(FinderBase):
    def __init__(self, loader_type=FilteringEvents.load_model(), get_type=Event):
        super(FinderEvent, self).__init__(loader_type, get_type)


class FindAll(FinderBase):
    def __init__(self, loader_type=[FilteringBooks.load_model(), FilteringEvents.load_model()], get_type=[Book, Event]):
        super(FindAll, self).__init__(loader_type, get_type)


class ColdStart:
    def __init__(self, k):
        self.k = k

    def find(self, request):
        books = Book.objects.all()
        books = books.order_by('-rating')
        k_book_to_go = books[0:self.k]

        events = LastEvent.objects.all()
        events = events.order_by('-score')
        ev_d = dict()
        for i in range(0, len(events)):
            if events[i].id_event.id in ev_d.keys():
                ev_d[events[i].id_event.id].append(events[i].score)
            else:
                ev_d[events[i].id_event.id] = [events[i].score]

        out = dict()
        for k, v in ev_d.items():
            avg = 0
            cnt = 0
            for score in v:
                if score:
                    avg += score
                    cnt += 1
            if cnt != 0:
                out[k] = avg / cnt

        out = {k: v for k, v in sorted(out.items(), key=lambda item: item[1], reverse=True)}
        out_keys = [Event.objects.get(id=k) for k, v in out.items()]
        k_event_to_go = out_keys[0:self.k]

        sections = LastSection.objects.all()
        sections = sections.order_by('-score')
        sec_d = dict()

        for i in range(0, len(sections)):
            if sections[i].id_section.id in sec_d.keys():
                sec_d[sections[i].id_section.id].append(sections[i].score)
            else:
                sec_d[sections[i].id_section.id] = [sections[i].score]

        out = dict()
        for k, v in sec_d.items():
            avg = 0
            cnt = 0
            for score in v:
                if score:
                    avg += score
                    cnt += 1
            if cnt != 0:
                out[k] = avg / cnt

        out = {k: v for k, v in sorted(out.items(), key=lambda item: item[1], reverse=True)}
        out_keys = [Section.objects.get(id=k) for k, v in out.items()]
        k_section_to_go = out_keys[0:self.k]

        dictAllInOne = dict()
        dictAllInOne['Books'] = k_book_to_go
        dictAllInOne['Events'] = k_event_to_go
        dictAllInOne['Sections'] = k_section_to_go
        return render(request, 'polls/index.html', dictAllInOne)


# events = LastEvent.objects.all()
# events = events.order_by('-score')
# ev_d = dict()
# for i in range(0, len(events)):
#     if events[i].id_event.id in ev_d.keys():
#         ev_d[events[i].id_event.id].append(events[i].score)
#     else:
#         ev_d[events[i].id_event.id] = [events[i].score]
#
# out = dict()
# for k, v in ev_d.items():
#     avg = 0
#     cnt = 0
#     for score in v:
#         if score:
#             avg += score
#             cnt += 1
#     if cnt != 0:
#         out[k] = avg / cnt
#
# out = {k: v for k, v in sorted(out.items(), key=lambda item: item[1], reverse=True)}
# out_keys = [Event.objects.get(id=k) for k, v in out.items()]
# # k_event_to_go = out_keys[0:self.k]
