from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from polls.models import *
from recommendation_system.FilteringModels import *
from polls.views import *

from polls.adder_last_object import *


def register(request):
    err = None
    if request.method == "POST":
        form = request.POST
        if form:
            username = form['username']
            tmp = User.objects.filter(user_login=username)
            if len(tmp) == 0:
                form = request.POST
                fName = form['first_name']
                lName = form['last_name']
                pwd1 = form['password1']
                age = form['age']
                User.objects.create(user_login=username, user_password=pwd1,
                                    first_name=fName, last_name=lName, age=age)
                fb = FilteringBooks.load_model()
                fb.update()
                fe = FilteringEvents.load_model()
                fe.update()
                fc = FilteringCulturalCenters.load_model()
                fc.update()

                return redirect(f'/registration/login')
            else:
                err = "This username is already exist"
    else:
        form = request.POST

    return render(request, "registration/signup.html", {"form": form, "error": err})


def login(request):
    err = None
    if request.method == "POST":
        form = request.POST
        print(form)
        username = form['username']
        pwd = form['password']
        try:
            user = User.objects.get(user_login=username, user_password=pwd)
        except User.DoesNotExist:
            user = None
            err = "User not found"
        if user:
            return recAll(request, id_user=user.id)
        else:
            return render(request, f'registration/login.html', {"form": form, 'error': err})
    else:
        form = request.POST
    return render(request, f'registration/login.html', {"form": form, 'error': err})


def logout(request):
    pass


def profile(request, id_user):
    if request.method == 'POST':
        post = request.POST
        type_ = post['type']
        if type_ == 'read_book':
            read_book(id_user, post['id_book'], status=1)
        if type_ == 'delete_book':
            read_book(id_user, post['id_book'], score=1, status=2)
        if type_ == 'visit_event':
            visit_event(id_user, post['id_event'], status=1)
        if type_ == 'delete_event':
            visit_event(id_user, post['id_event'], score=1, status=2)
        if type_ == 'visit_cultural_center':
            visit_cultural_center(id_user, post['id_cultural_center'], status=1)
        if type_ == 'delete_cultural_center':
            visit_cultural_center(id_user, post['id_cultural_center'], score=1, status=2)

    to_read = LastBook.objects.filter(id_user=id_user, status=0).values_list('id_book')
    to_read = [i[0] for i in to_read]
    to_read = Book.objects.filter(id__in=to_read)
    last_read = len(LastBook.objects.filter(id_user=id_user, status=1))

    to_event = LastEvent.objects.filter(id_user=id_user, status=0).values_list('id_event')
    to_event = [i[0] for i in to_event]
    to_event = Event.objects.filter(id__in=to_event)
    last_event = len(LastEvent.objects.filter(id_user=id_user, status=1))

    to_center = LastCenter.objects.filter(id_user=id_user, status=0).values_list('id_center')
    to_center = [i[0] for i in to_center]
    to_center = CultureCenter.objects.filter(id__in=to_center)
    last_center = len(LastCenter.objects.filter(id_user=id_user, status=1))

    return render(request, 'registration/profile.html', {'book': to_read, 'last_read': last_read,
                                                         'event': to_event, 'last_event': last_event,
                                                         'center': to_center, 'last_center': last_center,
                                                         'user': id_user})
