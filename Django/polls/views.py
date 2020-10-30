from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from recommendation_system.RequestModels import *
import numpy as np
from .finder import *


def index(request):
    finder = ColdStart(5)
    return finder.find(request)


def recommend(request, id_user):
    finder = FinderCenter()
    # finder = FinderBook()
    # finder = FinderEvent
    return finder.find(request, id_user)


def recAll(request, id_user):
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


from .forms import *


def book_searcher(request, id_user):
    authors = Book.objects.all().values_list('author')
    authors = [a[0] for a in authors]
    authors = list(np.unique(authors))
    genres = Genre.objects.all()

    if request.method == 'POST':
        rec_model = RequestModelBooks.load()
        print(request.POST)
        content = request.POST['content'][0]
        rec_list = rec_model.recommend(id_user, content)
        books = Book.objects.filter(id__in=rec_list)
        return render(request, 'polls/book_search.html',
                      {'ID_user': id_user, 'authors': authors, 'genres': genres, 'books': books})

    if request.method == 'GET':
        books = []
        get = request.GET
        print(get)
        filter_dict = {}
        if not len(get) == 0:
            author = get['author']
            genre =  int(get['genre']) if get['genre'].isdigit() else get['genre']
            print(author)
            print(genre)
            if not author == "Автор":
                filter_dict = {'author': author}
            if not genre == 'Жанр':

                book_id = GenreBook.objects.filter(genre=genre).values_list('book')
                book_id = [b[0] for b in book_id]
                filter_dict['id__in'] = book_id

            if 'sort_parametr' in get.keys():
                sort_paramer = get['sort_parametr']
                if sort_paramer == 'alphavit':
                    books = Book.objects.filter(**filter_dict).order_by('+title')
            else:
                books = Book.objects.filter(**filter_dict)
        return render(request, 'polls/book_search.html',
                      {'ID_user': id_user, 'authors': authors, 'genres': genres, 'books': books})
