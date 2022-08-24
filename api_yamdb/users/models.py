from django.contrib.auth.models import AbstractUser
from django.db import models
from reviews.choices import ROLE_CHOICES


class User(AbstractUser):
    role = models.CharField(
        choices=ROLE_CHOICES, max_length=10, default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.PositiveIntegerField(
        'Six digits code for getting access to token endpoint',
        null=True,
        blank=True,
    )
