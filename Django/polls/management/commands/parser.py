from tqdm import tqdm
from django.core.management.base import BaseCommand
from django.db import models
from polls.models import *
import pandas as pd
import numpy as np


class PreProcessingGenre:
    def make(self, genres):
        genres_set = set('')
        genres_books = []
        # Сделать множество всех жанров и списко жанров для каждой книги
        for genres_book_str in genres:
            genres_book_list = []
            genres_book_words_list = genres_book_str.split(' ')

            if list(genres_book_words_list) == 0:
                genres_book_list.append('')
                continue

            genre_name = genres_book_words_list[0]

            for word in genres_book_words_list:
                if word[0].isupper():
                    genres_book_list.append(genre_name)
                    genres_set.add(genre_name)
                    genre_name = word
                else:
                    genre_name += ' ' + word
            genres_book_list.append(genre_name)
            genres_set.add(genre_name)
            genres_books.append(genres_book_list)

        columns = list(genres_set)
        # Сделать df для жанров тип one hot encoding
        df_genre = pd.DataFrame(columns=columns)
        for genres_book in genres_books:
            row_val = [1 if genre in genres_book else 0 for genre in columns]
            row = dict(zip(columns, row_val))
            df_genre = df_genre.append(row, ignore_index=True)
        return df_genre


class GenreCreator:
    def create(self, genres):
        columns = genres.columns
        for id, column in tqdm(enumerate(columns), desc='Creating genres'):
            Genre.objects.create(id=id + 1, name=column)


class BookCreator:
    def create(self, df):
        for i, row in tqdm(df.iterrows(), desc='Creating books'):
            Book.objects.create(id=row['id'] + 1, title=row['name'], author=row['author'], serie=row['seria'],
                                rating=row['rating'],
                                pages=row['count_page'], language=row['language'], image=row['img_url'],
                                content=row['content'])


class BookGenreCreator:
    def create(self, df_genres):
        id_genre_book = 0
        for i, row in tqdm(df_genres.iterrows(), desc='Creating books genre'):
            list_ = list(row[row == 1].keys())
            book = Book.objects.get(id=i + 1)
            for genre in list_:
                id_genre_book += 1
                getted_genre = Genre.objects.get(name=genre)
                GenreBook.objects.create(id=id_genre_book, genre_id=getted_genre.id, book_id=book.id)


class LibraryCreator:
    def create(self, df):
        for i, row in tqdm(df.iterrows(), desc='Creating libraries'):
            Library.objects.create(id=row['id'] + 1, name=row['name'], type=row['type'], region=row['region'],
                                   location=row['location'], adress=row['adress'], latitude=row['latitude'],
                                   longitude=row['longitude'], phone_number=row['number'], web_site=row['site'],
                                   email=row['email'], social_net=row['social_networks'], work_time=row['time_work'],
                                   image=row['img_url'], content=row['content'])


class CenterCreator:
    def create(self, df):
        for i, row in tqdm(df.iterrows(), desc='Creating libraries'):
            CultureCenter.objects.create(id=row['id'] + 1, title=row['name'], web_site=row['offical_site'],
                                         underground=row['undegroud'], adress=row['adress'], number=row['number'],
                                         email=row['email'], social_net=row['social_netwoks'], latitude=row['latitude'],
                                         longitude=row['logitute'], image=row['img_url'], content=row['content'])


class Command(BaseCommand):
    help = '__Help__'

    def handle(self, *args, **options):
        if options['short']:
            print("Congrats!")
            print("You found easter egg!")
            print("Dat parsing doesn't work!!")
        elif options['parse__all']:
            print("\n...Start parsing...\n")
            df = pd.read_csv('../data/csv/books.csv')

            Book.objects.all().delete()
            book_creator = BookCreator()
            book_creator.create(df)

            Genre.objects.all().delete()
            prep = PreProcessingGenre()
            df_genre = prep.make(df.genre)
            genre_creator = GenreCreator()
            genre_creator.create(df_genre)

            GenreBook.objects.all().delete()
            book_genre_creator = BookGenreCreator()
            book_genre_creator.create(df_genre)

            df = pd.read_csv('../data/csv/libraries.csv')
            Library.objects.all().delete()
            library_creator = LibraryCreator()
            library_creator.create(df)

            df = pd.read_csv('../data/csv/cultural_centers.csv')
            CultureCenter.objects.all().delete()
            center_creator = CenterCreator()
            center_creator.create(df)

            print("\n...End parsing...\n")

        elif options['parse__book']:
            # book creating
            print("\n...Start parsing...\n")
            df = pd.read_csv('../data/csv/books.csv')
            Book.objects.all().delete()
            book_creator = BookCreator()
            book_creator.create(df)
            print("\n...End parsing...\n")

        elif options['parse__genre']:
            # genre creating
            print("\n...Start parsing...\n")
            df = pd.read_csv('../data/csv/books.csv')
            Genre.objects.all().delete()
            prep = PreProcessingGenre()
            df_genre = prep.make(df.genre)
            genre_creator = GenreCreator()
            genre_creator.create(df_genre)
            print("\n...End parsing...\n")

        elif options['parse__tuple__genre__book']:
            # book genre create
            print("\n...Start parsing...\n")
            df = pd.read_csv('../data/csv/books.csv')
            GenreBook.objects.all().delete()
            prep = PreProcessingGenre()
            df_genre = prep.make(df.genre)
            book_genre_creator = BookGenreCreator()
            book_genre_creator.create(df_genre)
            print("\n...End parsing...\n")

        elif options['parse__library']:
            # library create
            print("\n...Start parsing...\n")
            df = pd.read_csv('../data/csv/libraries.csv')
            Library.objects.all().delete()
            library_creator = LibraryCreator()
            library_creator.create(df)
            print("\n...End parsing...\n")

        elif options['parse__cultural__centers']:
            # cultural center create
            print("\n...Start parsing...\n")
            df = pd.read_csv('../data/csv/cultural_centers.csv')
            CultureCenter.objects.all().delete()
            center_creator = CenterCreator()
            center_creator.create(df)
            print("\n...End parsing...\n")

        elif options['parse__events']:
            # event create
            print("\n...Start parsing...\n")
            df = pd.read_csv('../data/csv/events.csv')
            Event.objects.all().delete()

            print("\n...End parsing...\n")

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--short',
            action='store_true',
            default=False,
            help='Easter egg'
        )

        parser.add_argument(
            '-p',
            '--parse--all',
            action='store_true',
            default=False,
            help='Parsing all data'
        )

        parser.add_argument(
            '-b',
            '--parse--book',
            action='store_true',
            default=False,
            help='Parsing books'
        )

        parser.add_argument(
            '-g',
            '--parse--genre',
            action='store_true',
            default=False,
            help='Parsing genres'
        )

        parser.add_argument(
            '-t',
            '--parse--tuple--genre--book',
            action='store_true',
            default=False,
            help='Parsing books genre'
        )

        parser.add_argument(
            '-l',
            '--parse--library',
            action='store_true',
            default=False,
            help='Parsing libraries'
        )

        parser.add_argument(
            '-c',
            '--parse--cultural--centers',
            action='store_true',
            default=False,
            help='Parsing events'
        )

        parser.add_argument(
            '-e',
            '--parse--events',
            action='store_true',
            default=False,
            help='Parsing events'
        )
