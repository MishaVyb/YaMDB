from django.db import models
from django.contrib.auth.models import AbstractUser
from reviews.choices import ROLE_CHOICES


class User(AbstractUser):

    role = models.CharField(choices=ROLE_CHOICES, max_length=10,
                            default=ROLE_CHOICES[0])
    bio = models.TextField(
        'Биография',
        blank=True,
    )
