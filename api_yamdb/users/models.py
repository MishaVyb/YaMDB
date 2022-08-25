from django.contrib.auth.models import AbstractUser
from django.db import models
from reviews.choices import ROLE_CHOICES


class User(AbstractUser):
    role = models.CharField(choices=ROLE_CHOICES, max_length=10,
                            default=ROLE_CHOICES[0])
    bio = models.TextField(
        'Биография',
        blank=True,
    )

class Confirmation(models.Model)
    username = models.CharField(max_length=150, unique=True)
    code = models.PositiveIntegerField(
        'Six digits code for getting access to token endpoint',
        null=True,
        blank=True,
    )
    issue_date = models.DateTimeField(auto_now_add=True)
