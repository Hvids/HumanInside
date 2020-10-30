from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from recommendation_system.RequestModels import *
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

    if request.method == 'POST':
        post = request.POST
        type_ = post['type']
        if type_ == 'book':
            add_last_book(id_user, post['id_book'])
        else:
            rec_model = RequestModelBooks.load()

            content = request.POST['content'][0]
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
                  {'ID_user': id_user, 'authors': authors, 'genres': genres, 'books': books})
