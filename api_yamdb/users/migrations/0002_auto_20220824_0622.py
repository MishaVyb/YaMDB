# Generated by Django 2.2.16 on 2022-08-24 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('admin', 'Администратор'), ('moderator', 'Модератор')], default=('user', 'Пользователь'), max_length=10),
        ),
    ]
