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


def add_last_book(id_user, id_book):
    book = Book.objects.get(id=id_book)
    user = User.objects.get(id=id_user)
    LastBook.objects.create(id_user=user, id_book=book, status=False, score=5)
    filter = FilteringBooks.load_model()
    filter.update()


def add_last_event(id_user, id_event):
    event = Event.objects.get(id=id_event)
    user = User.objects.get(id=id_user)
    LastEvent.objects.create(id_user=user, id_event=event, status=False, score=5)
    filter = FilteringEvents.load_model()

    filter.update()


def add_last_cultural_center(id_user, id_cultural_center):
    cultural_center = CultureCenter.objects.get(id=id_cultural_center)
    user = User.objects.get(id=id_user)
    LastCenter.objects.create(id_user=user, id_center=cultural_center, status=False, score=5)
    filter = FilteringCulturalCenters.load_model()
    filter.update()
    finder = FindAll()
