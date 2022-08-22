from django.db import models
from django.contrib.auth.models import AbstractUser
from reviews.choices import ROLE_CHOICES


class User(AbstractUser):

    role = models.CharField(choices=ROLE_CHOICES, max_length=10)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
