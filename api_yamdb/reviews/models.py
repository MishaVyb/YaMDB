import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.core import validators

User = get_user_model()


class Category(models.Model):
    """Модель таблицы Category."""

    name = models.CharField(max_length=256, verbose_name='Наименование')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель таблицы Genre."""

    name = models.CharField(max_length=256, verbose_name='Наименование')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель таблицы Title."""

    name = models.CharField(max_length=256, verbose_name='Наименование')
    year = models.IntegerField(verbose_name='Год выхода', db_index=True)
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория')
    genre = models.ManyToManyField(Genre,
                                   through='Genre_Title',
                                   verbose_name='Жанр')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def clean(self) -> None:
        if self.year > datetime.date.today().year:
            raise ValidationError('Год выхода не может быть позже текущего!')
        return super().clean()

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    """Модель таблицы Genre-Title."""

    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='Произведение')
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              verbose_name='Жанр')


class Review(models.Model):
    """Модель таблицы Review."""

    title = models.ForeignKey(Title,
                              related_name='reviews',
                              on_delete=models.CASCADE,
                              verbose_name='Произведение')
    text = models.TextField(verbose_name='Обзор')
    author = models.ForeignKey(User,
                               related_name='reviews',
                               on_delete=models.CASCADE,
                               verbose_name='Автор обзора')
    score = models.PositiveSmallIntegerField(verbose_name='Оценка',
                                validators=[validators.MinValueValidator(1,
                                    message='Оценка не может быть меньше 1!'),
                                validators.MaxValueValidator(10),
                                    message='Оцена не может быть больше 10!'])
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации обзора')

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text[:40]


class Comment(models.Model):
    """Модель таблицы Comment."""

    review = models.ForeignKey(Review,
                               related_name='comments',
                               on_delete=models.CASCADE,
                               verbose_name='Обзор')
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(User,
                               related_name='comments',
                               on_delete=models.CASCADE,
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['review']

    def __str__(self):
        return self.text[:40]
