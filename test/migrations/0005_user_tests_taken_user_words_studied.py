# Generated by Django 4.0.3 on 2022-05-07 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0004_rename_first_name_user_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tests_taken',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='words_studied',
            field=models.IntegerField(default=0),
        ),
    ]
