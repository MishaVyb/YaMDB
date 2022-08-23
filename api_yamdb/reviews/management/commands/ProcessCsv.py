from reviews.models import Category, Genre, Title, Genre_Title, Review, Comment, User
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.utils import IntegrityError
import csv
import os


FILE_TABLE = (
    ('users.csv', User),
    ('category.csv', Category),
    ('genre.csv', Genre),
    ('titles.csv', Title),
    ('genre_title.csv', Genre_Title),
    ('review.csv', Review),
    ('comments.csv', Comment),
)


class Command(BaseCommand):
    help = 'Загрузка тестовых данных из каталога static/data/'

    # def add_arguments(self, parser):
    #     parser.add_argument('--path', type=str, help="file path")
    #     parser.add_argument('--model_name', type=str, help="model name")
    #     parser.add_argument('--app_name', type=str, help="django app name that the model is connected to")

    # def handle(self, *args, **options):
    #     file_path = options['path']
    #     _model = get_model(options['app_name'], options['model_name'])
    #     with open(file_path, 'rb') as csv_file:
    #         reader = csv.reader(csv_file, delimiter=';', quotechar='|')
    #         header = next(reader)
    #         for row in reader:
    #             _object_dict = {key: value for key, value in zip(header, row)}
                # _model.objects.create(**_object_dict)

    def handle(self, *args, **options):
        for file_table in FILE_TABLE:
            _model = file_table[1]
            with open(os.path.join(settings.BASE_DIR, 'static/data',
                                   file_table[0]
                                  ), 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                header = next(csv_reader)
                for row in csv_reader:
                    _object_dict = {key: value for key, value in zip(header, row)}
                    # print(_object_dict)
                    try:
                        _model.objects.create(**_object_dict)
                    except IntegrityError:
                        pass
