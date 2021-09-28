# Generated by Django 3.2.6 on 2021-09-28 15:19

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0029_auto_20210928_0757'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(default='')),
                ('lemmas_pos', models.TextField(blank=True, default='')),
                ('tags', django_mysql.models.ListCharField(models.CharField(max_length=34), default='', max_length=175, size=5)),
            ],
        ),
    ]
