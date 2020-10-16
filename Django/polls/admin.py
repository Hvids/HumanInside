from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Event)
admin.site.register(CultureCenter)
admin.site.register(BooksInLibrary)
admin.site.register(LastBooks)
admin.site.register(LastEvents)
admin.site.register(Genre)
admin.site.register(GenreBook)
admin.site.register(Library)
