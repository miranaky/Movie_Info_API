from typing import OrderedDict

from django.test import TestCase

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

import pytest
from model_bakery import baker

from movies.models import Genre, Movie
from movies.serializers import MovieSerializer

pytestmark = pytest.mark.django_db


class TestMovieModel(TestCase):
    def setUp(self) -> None:
        if isinstance(Movie, type):
            self.movie = baker.make(Movie)

    def test_using_movie(self):
        self.assertIsInstance(self.movie, Movie)

    def test_movie_models_create(self):
        genre = baker.make(Genre, name="Documentary")
        movie = baker.make(
            Movie,
            title="Water",
            year="2020",
            genres=[genre],
            summary="Rejected by Hollywood.",
        )

        self.assertEqual(genre.name, "Documentary")
        self.assertEqual(movie.title, "Water")
        self.assertEqual(movie.year, "2020")
        self.assertEqual(movie.summary, "Rejected by Hollywood.")
        self.assertEqual(movie.genres.get(pk=genre.pk), genre)


class TestMovieSerializer(TestCase):
    def setUp(self):
        self.serializer = MovieSerializer

    @pytestmark
    def test_valid_serializer(self):
        genre = baker.make(Genre, name="Documentary")
        _data = {
            "title": "Fire",
            "year": "2019",
            "summary": "Fire is anywhere.",
            "genres": [
                genre,
            ],
        }
        result = {
            "id": 1,
            "title": "Fire",
            "year": "2019",
            "rating": 0,
            "summary": "Fire is anywhere.",
            "genres": [
                "Documentary",
            ],
        }
        serializer = self.serializer(data=_data)
        self.assertTrue(serializer.is_valid())
        serializer.save(genres=[genre])
        self.assertEqual(serializer.data, result)
        self.assertEqual(serializer.errors, {})

    @pytestmark
    def test_serializer_missing_title(self):
        genre = baker.make(Genre, name="Documentary")
        _data = {
            "year": "2019",
            "summary": "Fire is anywhere.",
            "genres": [
                genre,
            ],
        }

        serializer = self.serializer(data=_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {"title": ["This field is required."]})


class TestMovieInfoView(APITestCase):
    def create_movies(self):
        movie_data = [
            {
                "title": "Life of Pi",
                "year": "2012",
                "genres": ["Drama", "Adventure"],
                "summary": "Life of Pi is a 2012 adventure drama film[11] based on Yann Martel's 2001 novel of the same name.",
            },
            {
                "title": "CoCo",
                "year": "2017",
                "genres": ["Animation", "Adventure"],
                "summary": "Coco is a 2017 American computer-animated fantasy film produced by Pixar Animation Studios and released by Walt Disney Pictures.",
            },
        ]
        for input_json in movie_data:
            self.client.post(self.url, data=input_json, format="json")

    def create_reviews(self):
        review_url = "/api/v1/reviews/"
        review_data = [
            {"movie_id": 1, "text": "Bad Movie", "rating": 2},
            {"movie_id": 2, "text": "Greate Movie", "rating": 10},
            {"movie_id": 3, "text": "Good Movie", "rating": 7},
        ]
        for review in review_data:
            self.client.post(review_url, review, format="json")

    @pytestmark
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/v1/movies/"
        # create dummy movie
        self.genre_one, _ = Genre.objects.get_or_create(name="Documentary")
        self.genre_two, _ = Genre.objects.get_or_create(name="History")
        self._data = {
            "title": "The Fire",
            "year": "2019",
            "summary": "Fire is anywhere. It is problem.",
        }
        self.movie_instance = Movie.objects.create(**self._data)
        self.movie_instance.genres.set([self.genre_one, self.genre_two])

    @pytestmark
    def test_get_movie_list(self):
        response = self.client.get(self.url, content_type="application/json")
        result = {
            "id": 1,
            "title": "The Fire",
            "year": "2019",
            "rating": 0,
            "genres": [
                "Documentary",
                "History",
            ],
            "summary": "Fire is anywhere. It is problem.",
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0], OrderedDict(result))

    def test_get_movie_detail(self):
        url = f"{self.url}1/"
        response = self.client.get(url, content_type="application/json")
        result = {
            "id": 1,
            "title": "The Fire",
            "year": "2019",
            "rating": 0,
            "genres": [
                "Documentary",
                "History",
            ],
            "summary": "Fire is anywhere. It is problem.",
            "reviews": [],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data, OrderedDict(result))

    @pytestmark
    def test_post_movie(self):
        input_json = {
            "title": "Pushpa: The Rise",
            "year": "2021",
            "genres": ["Action", "Adventure"],
            "summary": "Story of Pushpa Raj, a lorry driver in Seshachalam forests of South India, set in the backdrop of red sandalwood smuggling. Red Sandalwood is endemic to South-Eastern Ghats (mountain range) of India.",
        }

        response = self.client.post(self.url, data=input_json, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @pytestmark
    def test_search_movie_title(self):
        url = f"{self.url}?title=Fire"
        response = self.client.get(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    @pytestmark
    def test_search_movie_title_not_exists(self):
        url = f"{self.url}?title=Water"
        response = self.client.get(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    @pytestmark
    def test_search_movie_genre(self):
        url = f"{self.url}?genres=History"
        response = self.client.get(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    @pytestmark
    def test_search_movie_genre_not_exist(self):
        url = f"{self.url}?genres=Horror"
        response = self.client.get(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    @pytestmark
    def test_search_movie_year(self):
        url = f"{self.url}?year=2021"
        response = self.client.get(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    @pytestmark
    def test_order_by_rating_descending(self):
        # create new movies
        self.create_movies()
        # create new reviiews
        self.create_reviews()
        # create reviews for order by rating
        url = f"{self.url}?order=descending"
        response = self.client.get(url, content_type="application/json")
        result = {
            "id": 2,
            "title": "Life of Pi",
            "year": "2012",
            "rating": 10,
            "genres": ["Drama", "Adventure"],
            "summary": "Life of Pi is a 2012 adventure drama film[11] based on Yann Martel's 2001 novel of the same name.",
        }
        print(response.data["results"][0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0], OrderedDict(result))

    @pytestmark
    def test_order_by_rating_ascending(self):
        # create new movies
        self.create_movies()
        # create new reviiews
        self.create_reviews()
        # create reviews for order by rating
        url = f"{self.url}?order=ascending"
        response = self.client.get(url, content_type="application/json")
        result = {
            "id": 1,
            "title": "The Fire",
            "year": "2019",
            "rating": 2,
            "genres": [
                "Documentary",
                "History",
            ],
            "summary": "Fire is anywhere. It is problem.",
        }
        print(response.data["results"][0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0], OrderedDict(result))
