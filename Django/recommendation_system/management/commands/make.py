from django.core.management.base import BaseCommand, CommandError
from polls.models import *
from .Maker import MakerMatrixUserTemp, MakerMatrixTemp, MakerMatrixBooks, MakerMatrixEvents, \
    MakerMatrixCulturalCenters, MakerMatrixLibraries


class Command(BaseCommand):
    help = "__Help__"

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--data',
            action='store_true',
            default=False,
            help='Make data for recommedation'
        )
        parser.add_argument(
            '-m',
            '--model',
            action='store_true',
            default=False,
            help='Make models recomedation'
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
                maker = MakerMatrixUserTemp(User, Temp, UserTemp)
                df = maker.make(name)
                maker.save_df(df, path, name)

        elif options['model']:

            path = './recommendation_system/data/'
            tuple_list = [
                (
                    'preprocessing_books.csv',
                    ['id', 'author', 'pages', 'rating', 'language', 'content'],
                    Book,
                    MakerMatrixBooks
                ),
                (
                    'preprocessing_events.csv',
                    ['id', 'town', 'price', 'age_rate', 'content'],
                    Event,
                    MakerMatrixEvents
                ),
                (
                    'preprocessing_cultural_centers.csv',
                    ['id', 'underground', 'latitude', 'longitude', 'content'],
                    CultureCenter,
                    MakerMatrixCulturalCenters
                ),
                (
                    'preprocessing_libraries.csv',
                    ['id', 'region', 'latitude', 'longitude', 'content'],
                    Library,
                    MakerMatrixLibraries
                )

            ]
            # event = Event.objects.all()
            # print(event[0])
            for name, select_columns, Temp, MakerTemp in tuple_list:
                maker = MakerMatrixTemp(Temp)
                maker_temp = MakerTemp()
                df = maker.make(select_columns)
                # print(df.head())
                df = maker_temp.make(df)
                maker.save_df(df, path, name)
