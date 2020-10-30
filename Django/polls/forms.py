from django import forms

from .models import Book

class PostSerachBooks(forms.Form):
    content = forms.CharField(label='content',max_length=255)