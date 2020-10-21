from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .functions import *
from recommendation_system.FilteringModels import *
from .finder import *


def index(request, id_book=3):
    method = Methods()
    return method.get_book(request, id_book)


def recommend(request, id_user):
    finder = FinderCenter()
    return finder.find(request, id_user)


def book_desc(request, id_book):
    book = Book.objects.get(id=id_book)
    return render(request, 'polls/index.html', {'book': book})

