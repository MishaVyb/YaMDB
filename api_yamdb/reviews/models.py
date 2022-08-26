from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Модель таблицы Category."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель таблицы Genre."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель таблицы Title."""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 null=True,
                                 on_delete=models.SET_NULL)
    genre = models.ManyToManyField(Genre,
                                    through='Genre_Title')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    """Модель таблицы Genre-Title."""

    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE)


class Review(models.Model):
    """Модель таблицы Review."""

    title = models.ForeignKey(Title,
                              related_name='reviews',
                              on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User,
                               related_name='reviews',
                               on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

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
                               on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User,
                               related_name='comments',
                               on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['review']

    def __str__(self):
        return self.text[:40]
