from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):

    title = models.CharField(max_length=180)
    year = models.CharField(max_length=4)
    summary = models.TextField()
    genres = models.ManyToManyField("Genre", related_name="movie", blank=True)

    def rating(self) -> int:
        rating = self.reviews.all().aggregate(models.Avg("rating")).get("rating__avg")
        if rating is None:
            rating = 0
        return rating

    def __str__(self):
        return self.title
