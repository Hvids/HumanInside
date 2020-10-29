from django import forms

from .models import Book

class PostLastBook(forms.ModelForm):
    class Meta:
        model= Book
        fields = ('title',)
