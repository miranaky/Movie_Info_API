# Generated by Django 4.0 on 2021-12-20 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='movie',
            new_name='movie_id',
        ),
    ]
