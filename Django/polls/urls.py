from django.urls import path

from . import views
from . import adder_last_object

urlpatterns = [
    path('', views.index, name='enter_page'),
    path('user/<int:id_user>/', views.recommend, name='recommendations'),
    path('home/user/<int:id_user>/', views.recAll, name='recAll'),
    path('home/user/<int:id_user>/book/<int:id_book>/', views.book_detail, name='book_detail'),
    path('home/user/<int:id_user>/event/<int:id_event>/', views.event_detail, name='event_detail'),
    path('home/user/<int:id_user>/center/<int:id_center>/', views.cultural_center_detail,
         name='cultural_center_detail'),
    path('search/user/<int:id_user>/books/', views.book_searcher, name='book_searcher'),

    # Добавка post Запросом и возврат на главную
    path('add_last_book/<int:id_user>/<int:id_book>/', adder_last_object.add_last_book, name='add_last_book'),
    path('add_last_event/<int:id_user>/<int:id_event>/', adder_last_object.add_last_event, name='add_last_event'),
    path('add_last_cultural_center/<int:id_user>/<int:id_cultural_center>/', adder_last_object.add_last_cultural_center,
         name='add_last_cultural_center'),
]
