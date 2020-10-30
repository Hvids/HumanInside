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
    finder = FinderCenter()
    # finder = FinderBook()
    # finder = FinderEvent
    return finder.find(request, id_user)


def recAll(request, id_user):
    if request.method == 'POST':
        print(request.POST)
        post = request.POST
        if post['type'] == 'delete_book':
            add_last_book(id_user, post['id_book'], status=True, score=1)
        elif post['type'] == 'delete_event':
            add_last_event(id_user, post['id_event'], status=True, score=1)
        elif post['type'] == 'delete_cultural_center':
            add_last_cultural_center(id_user, post['id_cultural_center'], status=True, score=1)
        else:
            add_last_object(post, id_user)

    finder = FindAll()
    return finder.findAll(request, id_user)


def book_detail(request, id_user, id_book):
    book = Book.objects.get(id=id_book)
    return render(request, 'polls/book.html', {'book': book, 'user': id_user})


def cultural_center_detail(request, id_user, id_center):
    cultural_center = CultureCenter.objects.get(id=id_center)
    return render(request, 'polls/CulturalCenter.html', {'cultural_center': cultural_center, 'user': id_user})


def event_detail(request, id_user, id_event):
    event = Event.objects.get(id=id_event)
    return render(request, 'polls/event.html', {'event': event, 'user': id_user})


def book_searcher(request, id_user):
    books = []
    authors = Book.objects.all().values_list('author')
    authors = [a[0] for a in authors]
    authors = list(np.unique(authors))
    genres = Genre.objects.all()

    cb = ContentBaseBooks.load()
    rec_ids_book = cb.recommend(id_user)
    recommend_book = Book.objects.filter(id__in=rec_ids_book)

    if request.method == 'POST':

        post = request.POST
        type_ = post['type']
        if type_ == 'book':
            add_last_book(id_user, post['id_book'])
        elif type_ == 'delete_book':
            add_last_book(id_user, post['id_book'], status=True, score=1)
        else:
            rec_model = RequestModelBooks.load()

            content = request.POST['content']
            print(content)
            rec_list = rec_model.recommend(id_user, content)
            books = Book.objects.filter(id__in=rec_list)

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
    ce = ContentBaseEvents.load()
    recommend_events = ce.recommend(id_user)
    recommend_events = Event.objects.filter(id__in=recommend_events)
    finder_events = []
    if request.method == 'POST':
        post = request.POST
        type = post['type']
        if type == 'search_rec':
            re = RequestModelEvents.load()
            content = post['content']
            finder_events = re.recommend(id_user, content)
            finder_events = Event.objects.filter(id__in=finder_events)
        elif type == 'filter_search':
            filter_dict = {}
            if not post['town'] == 'default':
                filter_dict['town'] = post['town']
            if not post['date'] == 'default':
                filter_dict['date'] = post['date']
            if not post['price'] == 'default':
                filter_dict['price'] = post['price']
            if not post['age_rate'] == 'default':
                filter_dict['age_rate'] = post['age_rate']
            if len(filter_dict.keys()) > 0:
                finder_events = Event.objects.filter(**filter_dict)
        elif type == 'event':
            add_last_event(id_user, post['id_event'])
        elif type == 'delete_event':
            add_last_event(id_user, post['id_event'], score=1, status=True)
    filter_parms = Event.objects.all().values_list('town', 'date', 'price', 'age_rate')
    towns = list(np.unique([t[0] for t in filter_parms]))
    dates = list(np.unique([t[1] for t in filter_parms]))
    prices = list(np.unique([t[2] for t in filter_parms]))
    age_rates = list(np.unique([t[3] for t in filter_parms]))

    return render(request, 'polls/event_search.html',
                  {
                      'ID_user': id_user,
                      'towns': towns,
                      'dates': dates,
                      'prices': prices,
                      'age_rates': age_rates,
                      'recommend_events': recommend_events,
                      "finder_events": finder_events
                  })
