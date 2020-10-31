from .finder import *
from .models import *
from recommendation_system.FilteringModels import *


def add_last_object(post, id_user):
    if post['type'] == 'book':
        add_last_book(id_user, post['id_book'])
    if post['type'] == 'event':
        add_last_event(id_user, post['id_event'])
    if post['type'] == 'cultural_center':
        add_last_cultural_center(id_user, post['id_cultural_center'])


def add_last_book(id_user, id_book, status=False, score=5):
    book = Book.objects.get(id=id_book)
    user = User.objects.get(id=id_user)
    LastBook.objects.create(id_user=user, id_book=book, status=status, score=score)
    filter_ = FilteringBooks.load_model()
    filter_.update()


def add_last_event(id_user, id_event, status=False, score=5):
    event = Event.objects.get(id=id_event)
    user = User.objects.get(id=id_user)
    LastEvent.objects.create(id_user=user, id_event=event, status=status, score=score)
    filter_ = FilteringEvents.load_model()

    filter_.update()


def add_last_cultural_center(id_user, id_cultural_center, status=False, score=5):
    cultural_center = CultureCenter.objects.get(id=id_cultural_center)
    user = User.objects.get(id=id_user)
    LastCenter.objects.create(id_user=user, id_center=cultural_center, status=status, score=score)
    filter_ = FilteringCulturalCenters.load_model()
    filter_.update()


def read_book(id_user, id_book, status=True, score=8):
    last_book = LastBook.objects.get(id_user=id_user, id_book=id_book)
    last_book.status = status
    last_book.score = score
    last_book.save()


def visit_event(id_user, id_event, status=True, score=8):
    last = LastEvent.objects.get(id_user=id_user, id_event=id_event)
    last.status = status
    last.score = score
    last.save()


def visit_cultural_center(id_user, id_cultural_center, status=True, score=8):
    last = LastCenter.objects.get(id_user=id_user, id_center=id_cultural_center)
    last.status = status
    last.score = score
    last.save()
