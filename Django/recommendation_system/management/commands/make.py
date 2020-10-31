from django.core.management.base import BaseCommand
from polls.models import *

from recommendation_system.Maker import *


class Command(BaseCommand):
    help = "__Help__"

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            default=False,
            help='Make all'
        )
        parser.add_argument(
            '-s',
            '--similar',
            action='store_true',
            default=False,
            help='Make similar json'
        )
        parser.add_argument(
            '-m',
            '--filtering--matrix',
            action='store_true',
            default=False,
            help='Make data for coloborative filtering'
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
        if options['filtering__matrix']:
            self.make_filtering_matrix()
        elif options['preprocessing']:
            self.make_preprocessing_matirx()
        elif options['filter__models']:
            self.make_filtering_models()
        elif options['similar']:
            self.make_similar_json()
        elif options['all']:
            self.make_filtering_matrix()
            self.make_preprocessing_matirx()
            self.make_similar_json()
            self.make_filtering_models()

    def make_filtering_matrix(self):
        print('Make Filtering Matrix')
        MakerObjects = [MakerFilteringMatrixBooks, MakerFilteringMatrixEvents, MakerFilteringMatrixSections]
        for MakerObject in MakerObjects:
            maker = MakerObject()
            maker.make()

    def make_preprocessing_matirx(self, fit=False):
        print('Make Preprocessing Matrix')
        # MakerObjects = [MakerMatrixPreprocessingBooks, MakerMatrixPreprocessingEvents,
        #                 MakerMatrixPreprocessingSections]
        MakerObjects = [MakerMatrixPreprocessingSections]
        for MakerObject in MakerObjects:
            maker = MakerObject()
            maker.make(fit=fit)

    def make_similar_json(self):
        print('Make Similar JSON')
        MakerObjects = [MakerSimilarJSONBooks, MakerSimilarJSONEvents, MakerFilteringModelSections]
        for MakerObject in MakerObjects:
            maker = MakerObject()
            maker.make()

    def make_filtering_models(self):
        print('Make Filtering Models')
        MakerObjects = [MakerFilteringModelBooks, MakerFilteringModelEvents, MakerFilteringModelSections]
        for MakerObject in MakerObjects:
            maker = MakerObject()
            maker.make()
