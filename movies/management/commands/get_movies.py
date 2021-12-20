from typing import Any
from django.core.management.base import BaseCommand

import requests

from movies.models import Movie, Genre


class Command(BaseCommand):
    help = "This command creates movies from yts.mx"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit", default=20, type=int, help="The limit of movie results per page that has been set"
        )
        parser.add_argument("--max_page", default=5, type=int, help="Page to explore as much as possible")

    def handle(self, *args: Any, **options: Any):
        limit = options.get("limit")
        max_page = options.get("max_page")
        count = 0

        for page in range(1, max_page + 1):
            self.stdout.write(self.style.HTTP_INFO(f"Getting Movies info from {page} page"))
            payload = {"page": page, "limit": limit}
            url = "https://yts.mx/api/v2/list_movies.json"
            res = requests.get(url, params=payload)
            movies = res.json().get("data").get("movies")
            for movie in movies:
                _movie = {
                    "title": movie.get("title"),
                    "year": movie.get("year"),
                    "summary": movie.get("summary"),
                }
                if not Movie.objects.filter(title=_movie.get("title"), year=_movie.get("year")):
                    instance = Movie.objects.create(**_movie)
                    genres = []
                    if movie.get("genres") is not None:
                        for genre in movie.get("genres"):
                            genre, _ = Genre.objects.get_or_create(name=genre)
                            genres.append(genre)
                        instance.genres.set(genres)
                    count += 1

        if count > 0:
            self.stdout.write(self.style.SUCCESS(f"{count} Movies Added!"))

        else:
            self.stdout.write(self.style.WARNING(f"There is no new movie to add."))
