from .models import *


def make_list(l):
    return [i[0] for i in l]

from django.db.models import Q


def search_book(id_user, filter_dict, order_title=False):
    books_read_user = LastBook.objects.filter(id_user=id_user).values_list('id_book')
    books_read_user = make_list(books_read_user)
    books_read_user = Book.objects.filter(**filter_dict).filter(~Q(id__in=books_read_user))
    if order_title:
        books_read_user = books_read_user.order_by('+title')
    return books_read_user
