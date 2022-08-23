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
                    try:
                        _model.objects.create(**_object_dict)
                    except IntegrityError:
                        pass
