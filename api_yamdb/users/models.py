from core import descriptors
from django.contrib.auth.models import AbstractUser
from django.db import models


class _UserRoleChoices:
    USER = descriptors.Constant('user')
    MODERATOR = descriptors.Constant('moderator')
    ADMIN = descriptors.Constant('admin')

    @classmethod
    def get_choices_list(cls):
        return (
            (cls.USER, 'пользователь'),
            (cls.MODERATOR, 'модератор'),
            (cls.ADMIN, 'администратор'),
        )


class User(AbstractUser):
    ROLE_CHOICES = _UserRoleChoices()

    role = models.CharField(
        choices=_UserRoleChoices.get_choices_list(),
        max_length=10,
        default=ROLE_CHOICES.USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == self.ROLE_CHOICES.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.ROLE_CHOICES.MODERATOR

    @property
    def is_user(self):
        return self.role == self.ROLE_CHOICES.USER

    class Meta:
        ordering = ['last_name', 'first_name']


class Confirmation(models.Model):

    username = models.CharField(max_length=150, unique=True)

    code = models.PositiveIntegerField(
        'Six digits code for getting access to token endpoint',
        null=True,
        blank=True,
    )
    issue_date = models.DateTimeField(auto_now_add=True)
