# Generated by Django 3.2.6 on 2022-03-27 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0038_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
