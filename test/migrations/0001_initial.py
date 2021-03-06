# Generated by Django 3.2.6 on 2022-03-27 15:49

from django.db import migrations, models
import django_mysql.models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lemma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=34)),
                ('freq', models.IntegerField(default=0)),
                ('def_en', models.TextField(blank=True, default='')),
                ('def_zh', models.TextField(blank=True, default='')),
                ('sent_ids', jsonfield.fields.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Passage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(blank=True, default='', max_length=100)),
                ('text', models.TextField(default='')),
                ('lemma_pos', models.TextField(blank=True, default='')),
                ('counter', models.IntegerField(default=0)),
                ('difficulty', models.FloatField(blank=True, default=0)),
                ('tags', django_mysql.models.ListCharField(models.CharField(max_length=34), blank=True, default='', max_length=175, size=5)),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passage_id', models.IntegerField(default=0)),
                ('text', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=15)),
                ('last_name', models.CharField(default='', max_length=15)),
                ('password', models.CharField(default='', max_length=32)),
                ('language_code', models.CharField(default='', max_length=2)),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=34)),
                ('lem_id', models.IntegerField(default=0)),
            ],
        ),
    ]
