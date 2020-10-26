from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='Enter page'),
    path('user/<int:id_user>/', views.recommend, name='recommendations'),
    path('home/user/<int:id_user>/', views.recAll, name='recAll'),
    path('home/user/<int:id_user>/book/<int:id_book>/', views.book_detail, name='book_detail'),
    path('home/user/<int:id_user>/event/<int:id_event>/', views.event_detail, name='event_detail'),
    path('home/user/<int:id_user>/center/<int:id_center>/', views.cultural_center_detail, name='cultural_center_detail'),
]
