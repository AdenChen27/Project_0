# Generated by Django 3.2.6 on 2021-08-19 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0008_auto_20210810_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='appear_cnt',
            field=models.IntegerField(default=0),
        ),
    ]
