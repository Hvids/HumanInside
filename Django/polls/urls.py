from django.urls import path

from . import views
from . import adder_last_object

urlpatterns = [
    path('', views.index, name='enter_page'),
    path('user/<int:id_user>/', views.recommend, name='recommendations'),
    path('home/user/<int:id_user>/', views.recAll, name='recAll'),
    path('home/user/<int:id_user>/book/<int:id_book>/', views.book_detail, name='book_detail'),
    path('home/user/<int:id_user>/event/<int:id_event>/', views.event_detail, name='event_detail'),
    path('home/user/<int:id_user>/section/<int:id_event>/', views.section_detail, name='section_detail'),
    #  поиск
    path('search/user/<int:id_user>/books/', views.book_searcher, name='book_searcher'),
    path('search/user/<int:id_user>/events/', views.event_searcher, name='event_searcher'),
    path('search/user/<int:id_user>/section/', views.section_searcher, name='section_searcher'),

]
