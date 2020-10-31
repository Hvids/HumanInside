from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(GenreBook)
admin.site.register(Library)
admin.site.register(BooksInLibrary)
admin.site.register(Event)
admin.site.register(Section)
admin.site.register(LastBook)
admin.site.register(LastEvent)
admin.site.register(LastSection)
