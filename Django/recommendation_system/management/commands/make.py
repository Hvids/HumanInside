from django.core.management.base import BaseCommand, CommandError
from polls.models import *
from .Maker import MakerMatrixUserTemp, MakerMatrixTemp, MakerMatrixBooks, MakerMatrixEvents, \
    MakerMatrixCulturalCenters, MakerMatrixLibraries, MakerFilteringModels, MakerSimilarJson
from tqdm import tqdm


class Command(BaseCommand):
    help = "__Help__"

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--similar',
            action='store_true',
            default=False,
            help='Make similar json'
        )
        parser.add_argument(
            '-d',
            '--data',
            action='store_true',
            default=False,
            help='Make data for recommedation'
        )
        parser.add_argument(
            '-p',
            '--preprocessing',
            action='store_true',
            default=False,
            help='Make preprocessing data '
        )
        parser.add_argument(
            '-f',
            '--filter--models',
            action='store_true',
            default=False,
            help='Make recommend model '
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

        elif options['preprocessing']:

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
            for name, select_columns, Temp, MakerTemp in tuple_list:
                maker = MakerMatrixTemp(Temp)
                maker_temp = MakerTemp()
                df = maker.make(select_columns)
                con, df = maker_temp.make(df)
                maker.save_df(df, path, name)
                maker.save_df(con, path, 'content_' + name)
        elif options['filter__models']:
            maker = MakerFilteringModels()
            names = ['users_books', 'users_cultural_centers', 'users_events']
            for name in tqdm(names, desc='Filter Models Create'):
                maker.make(name)
        elif options['similar']:

            maker = MakerSimilarJson()
            names = ['books', 'cultural_centers', 'events']
            for name in names:
                res = maker.make(name)
                maker.save_json(res, name)

        elif options['content']:

            maker = MakerSimilarJson()
            names = ['books', 'cultural_centers', 'events']
            for name in names:
                res = maker.make(name)
                maker.save_json(res, name)
