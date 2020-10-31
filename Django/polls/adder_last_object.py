from .finder import *
from .models import *
from recommendation_system.FilteringModels import *


def add_last_object(post, id_user):
    if post['type'] == 'book':
        add_last_book(id_user, post['id_book'], status=0)
    if post['type'] == 'event':
        add_last_event(id_user, post['id_event'], status=0)


def add_last_book(id_user, id_book, status=0, score=5):
    book = Book.objects.get(id=id_book)
    user = User.objects.get(id=id_user)
    LastBook.objects.create(id_user=user, id_book=book, status=status, score=score)
    filter_ = FilteringBooks.load_model()
    filter_.update()


def add_last_event(id_user, id_event, status=0, score=5):
    event = Event.objects.get(id=id_event)
    user = User.objects.get(id=id_user)
    LastEvent.objects.create(id_user=user, id_event=event, status=status, score=score)
    filter_ = FilteringEvents.load_model()

    filter_.update()


def read_book(id_user, id_book, status=1, score=8):
    last_book = LastBook.objects.get(id_user=id_user, id_book=id_book)
    last_book.status = status
    last_book.score = score
    last_book.save()


def visit_event(id_user, id_event, status=1, score=8):
    last = LastEvent.objects.get(id_user=id_user, id_event=id_event)
    last.status = status
    last.score = score
    last.save()

