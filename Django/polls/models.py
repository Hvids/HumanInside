from django.db import models
from django.utils import timezone
from django.conf import settings


class BooksInLibrary(models.Model):
    id_book = models.ForeignKey('Book', on_delete=models.CASCADE)
    id_library = models.ForeignKey('Library', on_delete=models.CASCADE)

    def __str__(self):
        return f'ID: {self.id}, ID book: {self.id_book}, ID library: {self.id_library}'


class LastBook(models.Model):
    id_user = models.ForeignKey('User', on_delete=models.CASCADE)
    id_book = models.ForeignKey('Book', on_delete=models.CASCADE)
    status = models.IntegerField()
    score = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f'ID: {self.id}, ID user: {self.id_user}, ID book: {self.id_book},' \
               f' status: {self.status}, score{self.score}'


class LastEvent(models.Model):
    id_event = models.ForeignKey('Event', on_delete=models.CASCADE)
    id_user = models.ForeignKey('User', on_delete=models.CASCADE)
    status = models.IntegerField()
    score = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f'ID: {self.id}, ID event: {self.id_event}, ID user: {self.id_user},' \
               f' status: {self.status} score{self.score}'


class User(models.Model):
    user_login = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self):
        return f'ID: {self.id}, login: {self.user_login}, password: {self.user_password},' \
               f' first name: {self.first_name}, last name: {self.last_name}, age: {self.age}'


class Event(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    name_center = models.CharField(max_length=255)
    type_center = models.CharField(max_length=255)
    name_district = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    type_event = models.CharField(max_length=255)
    follow_event = models.CharField(max_length=255)
    holiday = models.CharField(max_length=255)
    name_holiday = models.CharField(max_length=255)
    date_start = models.CharField(max_length=255)
    time_start = models.CharField(max_length=255)
    date_end = models.CharField(max_length=255)
    time_end = models.CharField(max_length=255)
    content = models.TextField()
    age_rate = models.CharField(max_length=255)
    age_category = models.CharField(max_length=255)
    goal_auditory = models.CharField(max_length=255)

    def __str__(self):
        return f'ID: {self.id}, title: {self.title}'


class LastSection(models.Model):
    id_user = models.ForeignKey('User', on_delete=models.CASCADE)
    id_section = models.ForeignKey('Section', on_delete=models.CASCADE)
    status = models.IntegerField()
    score = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f'ID: {self.id}, ID event: {self.id_section}, ID user: {self.id_user},' \
               f' status: {self.status} score{self.score}'


class Section(models.Model):
    title = models.CharField(max_length=255)
    type_price = models.CharField(max_length=255)
    type_schedule = models.CharField(max_length=255)
    time_learn = models.CharField(max_length=255)
    one_duration = models.CharField(max_length=255)
    name_org = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    underground = models.CharField(max_length=255)

    def __str__(self):
        return f'ID: {self.id}, title: {self.title}'


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'ID: {self.id}, name: {self.name}'


class GenreBook(models.Model):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return f'ID: {self.id}, genre: {self.genre}, book: {self.book}'


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    serie = models.CharField(max_length=255)
    rating = models.FloatField()
    pages = models.IntegerField()
    language = models.CharField(max_length=255)
    image = models.URLField()
    content = models.TextField()

    def __str__(self):
        return f'ID: {self.id}, title: {self.title}, author: {self.author}, serie: {self.serie}, ' \
               f'rating: {self.rating}, language: {self.language}, image: {self.image},' \
               f'\n content: {self.content}'


class Library(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    adress = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone_number = models.CharField(max_length=255)
    web_site = models.URLField()
    email = models.EmailField()
    social_net = models.TextField()
    work_time = models.TextField()
    image = models.URLField()
    content = models.TextField()

    def __str__(self):
        return f'ID: {self.id}, name: {self.name}, type: {self.type}, region: {self.region}, location: ' \
               f'{self.location}, adress: {self.adress}, latitude: {self.latitude}, ' \
               f'longitude: {self.longitude}, phone_number: {self.phone_number}, social net: {self.social_net},' \
               f' work time: {self.work_time}, image: {self.image},' \
               f'\n content: {self.content}'
