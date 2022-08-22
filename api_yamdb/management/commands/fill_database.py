from reviews.models import Category, Genre, Title, Genre_Title, Review, Comments, User
from django.core.management.base import BaseCommand
from django.conf import settings
import csv
import os


FILE_TABLE = (
    ('users.csv', 'user'),
    ('category.csv', 'category'),
    ('genre.csv', 'genre'),
    ('title.csv', 'title'),
    ('genre_title.csv', 'genre_title'),
    ('review.csv', 'review'),
    ('comments.csv', 'comment'),
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.join.path(settings.STATICFILES_DIR / 'data/your_csv_file.csv'), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                Product.objects.create(
                    name=row[2], description=row[3], price=row[4])



