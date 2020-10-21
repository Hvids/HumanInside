from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='Polls page'),
    path('user/<int:id_user>/', views.recommend, name='recommendations'),
    # ex: /polls/5/
    path('<int:id_book>/', views.book_desc, name='book_desc'),
]
