from .models import *
from django.db.models import Q
from Levenshtein import *


def make_list(l):
    return [i[0] for i in l]


def search_book(id_user, filter_dict, order_title=False):
    books_read_user = LastBook.objects.filter(id_user=id_user).values_list('id_book')
    books_read_user = make_list(books_read_user)
    books_read_user = Book.objects.filter(**filter_dict).filter(~Q(id__in=books_read_user))
    if order_title:
        books_read_user = books_read_user.order_by('+title')
    return books_read_user


def search_by_name(pattern, obj_type):
    elements = obj_type.objects.all()
    titles = [(element.title, element.id) for element in elements]

    match = []
    for title, id_ in titles:
        if title.find(pattern) != -1:
            match.append((title, id_))

    if len(match) != 0:
        all_id_in_match = [i[1] for i in match]
        return all_id_in_match

    all_distance = [(distance(pattern, title[0]), title[1]) for title in titles]
    sorted(all_distance, key=lambda x: x[0])

    all_id_in_distance = [i[1] for i in all_distance]
    all_id_in_distance = all_id_in_distance[0:5]
    return all_id_in_distance
