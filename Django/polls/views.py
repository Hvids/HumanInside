from django.shortcuts import render
from django.http import HttpResponse
from .models import *
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


def book_searcher(request, id_user):
    return render(request, 'polls/book_search.html', {'user': id_user})
