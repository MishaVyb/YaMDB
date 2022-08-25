# Generated by Django 2.2.16 on 2022-08-25 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_merge_20220825_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('code', models.PositiveIntegerField(blank=True, null=True, verbose_name='Six digits code for getting access to token endpoint')),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
    ]
