from tqdm import tqdm
from django.core.management.base import BaseCommand
from polls.models import *
from django.shortcuts import render
from django.http import HttpResponse


class Methods:
    def get_book(self, request, id_book):
        book = Book.objects.get(id=id_book)
        return render(request, 'polls/index.html', {'book': book})
