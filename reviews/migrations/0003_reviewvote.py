# Generated by Django 4.0 on 2021-12-20 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_rename_movie_review_movie_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_vote', to='reviews.review')),
            ],
        ),
    ]
