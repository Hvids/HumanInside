from django.urls import path, include

from registration import views as reg_views

urlpatterns = [
    path('login/', reg_views.login, name='login'),
    path('logout/', reg_views.logout, name='logout'),
    path('register/', reg_views.register, name="register"),
    path('profile/user/<int:id_user>/', reg_views.profile, name='profile'),
    path('', include("django.contrib.auth.urls")),
]
