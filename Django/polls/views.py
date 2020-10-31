from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from recommendation_system.RequestModels import *
from recommendation_system.ContentBaseModels import *
import numpy as np
from .finder import *
from .adder_last_object import *
from .forms import *
from .Searcher import *


def index(request):
    finder = ColdStart(5)
    return finder.find(request)


def recommend(request, id_user):
    finder = FinderBook()
    # finder = FinderEvent
    return finder.find(request, id_user)


def recAll(request, id_user):
    if request.method == 'POST':
        print(request.POST)
        post = request.POST
        if post['type'] == 'delete_book':
            add_last_book(id_user, post['id_book'], status=2, score=1)
        elif post['type'] == 'delete_event':
            add_last_event(id_user, post['id_event'], status=2, score=1)
        elif post['type'] == 'delete_section':
            add_last_section(id_user, post['id_section'], status=2, score=1)
        else:
            add_last_object(post, id_user)

    finder = FindAll()
    return finder.findAll(request, id_user)


def book_detail(request, id_user, id_book):
    book = Book.objects.get(id=id_book)
    return render(request, 'polls/book.html', {'book': book, 'user': id_user})


def event_detail(request, id_user, id_event):
    event = Event.objects.get(id=id_event)
    return render(request, 'polls/event.html', {'event': event, 'user': id_user})


def section_detail(request, id_user, id_section):
    section = Section.objects.get(id=id_section)
    return render(request, 'polls/section.html', {'section': section, 'user': id_user})


def book_searcher(request, id_user):
    books = []
    authors = Book.objects.all().values_list('author')
    authors = [a[0] for a in authors]
    authors = list(np.unique(authors))
    genres = Genre.objects.all()

    if request.method == 'POST':

        post = request.POST
        type_ = post['type']
        if type_ == 'book':
            add_last_book(id_user, post['id_book'], status=0)
        elif type_ == 'delete_book':
            add_last_book(id_user, post['id_book'], status=2, score=1)
        else:
            rec_model = RequestModelBooks.load()

            content = request.POST['content']
            print(content)
            rec_list = rec_model.recommend(id_user, content)
            books = Book.objects.filter(id__in=rec_list)

    cb = ContentBaseBooks.load()
    rec_ids_book = cb.recommend(id_user)
    recommend_book = Book.objects.filter(id__in=rec_ids_book)

    if request.method == 'GET':

        get = request.GET
        filter_dict = {}
        if not len(get) == 0:
            author = get['author']
            genre = int(get['genre']) if get['genre'].isdigit() else get['genre']
            if not author == "Автор":
                filter_dict = {'author': author}
            if not genre == 'Жанр':
                book_id = GenreBook.objects.filter(genre=genre).values_list('book')
                book_id = [b[0] for b in book_id]
                filter_dict['id__in'] = book_id

            if 'sort_parametr' in get.keys():
                sort_parametr = get['sort_parametr']
                if sort_parametr == 'alphavit':
                    books = search_book(id_user, filter_dict, order_title=True)
            else:
                books = search_book(id_user, filter_dict, order_title=False)
    return render(request, 'polls/book_search.html',
                  {'ID_user': id_user, 'authors': authors, 'genres': genres, 'books': books,
                   'recommend_book': recommend_book})


def event_searcher(request, id_user):
    finder_events = []
    if request.method == 'POST':
        post = request.POST
        type_ = post['type']
        if type_ == 'search_rec':
            re = RequestModelEvents.load()
            content = post['content']
            finder_events = re.recommend(id_user, content)
            finder_events = Event.objects.filter(id__in=finder_events)
        elif type_ == 'filter_search':
            filter_dict = {}
            if not post['type_center'] == 'default':
                filter_dict['type_center'] = post['type_center']
            if not post['price'] == 'default':
                filter_dict['price'] = post['price']
            if not post['type_event'] == 'default':
                filter_dict['type_event'] = post['type_event']
            if not post['holiday'] == 'default':
                filter_dict['holiday'] = post['holiday']
            if not post['age_rate'] == 'default':
                filter_dict['age_rate'] = post['age_rate']
            if len(filter_dict.keys()) > 0:
                finder_events = Event.objects.filter(**filter_dict)
        elif type_ == 'event':
            add_last_event(id_user, post['id_event'], status=0)
        elif type_ == 'delete_event':
            add_last_event(id_user, post['id_event'], score=1, status=2)
    filter_parms = Event.objects.all().values_list('type_center', 'price', 'type_event', 'holiday', 'age_rate')
    type_centers = list(np.unique([t[0] for t in filter_parms]))
    prices = list(np.unique([t[1] for t in filter_parms]))
    type_events = list(np.unique([t[2] for t in filter_parms]))
    holidays = list(np.unique([t[3] for t in filter_parms]))
    age_rates = list(np.unique([t[4] for t in filter_parms]))
    ce = ContentBaseEvents.load()
    recommend_events = ce.recommend(id_user)
    recommend_events = Event.objects.filter(id__in=recommend_events)
    return render(request, 'polls/event_search.html',
                  {
                      'ID_user': id_user,
                      'type_centers': type_centers,
                      'prices': prices,
                      'type_events': type_events,
                      'holidays': holidays,
                      'age_rates': age_rates,
                      'recommend_events': recommend_events,
                      "finder_events": finder_events
                  })


def section_searcher(request, id_user):
    pass
#     section_events = []
#     if request.method == 'POST':
#         post = request.POST
#         type_ = post['type']
#         if type_ == 'search_rec':
#             re = RequestModelEvents.load()
#             content = post['content']
#             finder_sections = re.recommend(id_user, content)
#             finder_sections = Event.objects.filter(id__in=finder_sections)
#         elif type_ == 'filter_search':
#             filter_dict = {}
#             if not post['town'] == 'default':
#                 filter_dict['town'] = post['town']
#             if not post['date'] == 'default':
#                 filter_dict['date'] = post['date']
#             if not post['price'] == 'default':
#                 filter_dict['price'] = post['price']
#             if not post['age_rate'] == 'default':
#                 filter_dict['age_rate'] = post['age_rate']
#             if len(filter_dict.keys()) > 0:
#                 finder_sections = Event.objects.filter(**filter_dict)
#         elif type_ == 'event':
#             add_last_event(id_user, post['id_event'], status=0)
#         elif type_ == 'delete_event':
#             add_last_event(id_user, post['id_event'], score=1, status=2)
#     filter_parms = Event.objects.all().values_list('town', 'date', 'price', 'age_rate')
#     towns = list(np.unique([t[0] for t in filter_parms]))
#     dates = list(np.unique([t[1] for t in filter_parms]))
#     prices = list(np.unique([t[2] for t in filter_parms]))
#     age_rates = list(np.unique([t[3] for t in filter_parms]))
#     ce = ContentBaseEvents.load()
#     recommend_events = ce.recommend(id_user)
#     recommend_events = Event.objects.filter(id__in=recommend_events)
#     return render(request, 'polls/event_search.html',
#                   {
#                       'ID_user': id_user,
#                       'towns': towns,
#                       'dates': dates,
#                       'prices': prices,
#                       'age_rates': age_rates,
#                       'recommend_events': recommend_events,
#                       "finder_sections": finder_sections
#                   })
