# Generated by Django 2.2.16 on 2022-08-23 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220823_1850'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['review'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['title'], 'verbose_name': 'Обзор', 'verbose_name_plural': 'Обзоры'},
        ),
    ]
