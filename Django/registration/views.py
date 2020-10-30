from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from polls.models import *
from recommendation_system.FilteringModels import *
from polls.views import *

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
