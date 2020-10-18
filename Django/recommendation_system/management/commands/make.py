from django.core.management.base import BaseCommand, CommandError
from polls.models import *
from .Maker import MakerMatrix


class Command(BaseCommand):
    help = "__Help__"

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--data',
            action='store_true',
            default=False,
            help='Easter egg'
        )

    def handle(self, *args, **options):
        if options['data']:
            path = './recommendation_system/data/'
            # Таблица пользователи и книги
            tuple_list = [
                ('users_books.csv', Book, LastBook),
                ('users_events.csv', Event, LastEvent),
                ('users_cultural_centers.csv', CultureCenter, LastCenter),

            ]
            for name, Temp, UserTemp in tuple_list:
                maker = MakerMatrix(User, Temp, UserTemp)
                df = maker.make(name)
                maker.save_df(df, path, name)
