from typing import OrderedDict

from django.test import TestCase

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

import pytest
from model_bakery import baker

from movies.models import Movie
from reviews.models import Review, ReviewVote

pytestmark = pytest.mark.django_db


class TestReviewModel(TestCase):
    def setUp(self) -> None:
        self.movie = baker.make(Movie)
        if isinstance(Review, type):
            self.review = baker.make(Review)

    def test_using_review(self) -> None:
        self.assertIsInstance(self.review, Review)

    def test_review_models_create(self) -> None:
        review = baker.make(
            Review,
            movie_id=self.movie,
            text="Good Movie",
            rating=8,
        )

        self.assertEqual(review.text, "Good Movie")
        self.assertEqual(review.rating, 8)
        self.assertEqual(review.movie_id, self.movie)


class TestReviewVoteModel(TestCase):
    def setUp(self) -> None:
        if isinstance(ReviewVote, type):
            self.review_vote = baker.make(ReviewVote)
        self.review_one = baker.make(Review)
        self.review_two = baker.make(Review)

    def test_using_review(self) -> None:
        self.assertIsInstance(self.review_vote, ReviewVote)

    def test_review_vote_models_create(self) -> None:
        review_vote = baker.make(
            ReviewVote,
            review_id=self.review_one,
        )

        self.assertEqual(review_vote.review_id, self.review_one)
        self.assertEqual(self.review_one.vote, 1)
        self.assertEqual(self.review_two.vote, 0)


class TestReviewView(APITestCase):
    @pytestmark
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/v1/reviews/"
        self.movie = baker.make(Movie)
        self.review_one = baker.make(
            Review,
            movie_id=self.movie,
            text="Good Movie",
            rating=8,
        )
        self.review_two = baker.make(Review)
        self.review_three = baker.make(Review)

    @pytestmark
    def test_get_review_detail(self):
        url = f"{self.url}1/"
        response = self.client.get(url, content_type="application/json")
        result = {"id": 1, "text": "Good Movie", "rating": 8, "vote": 0}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        response.data.pop("created_at")
        response.data.pop("updated_at")
        self.assertEqual(response.data, result)

    @pytestmark
    def test_post_review(self):
        json_data = {
            "movie_id": 1,
            "text": "Exciting Movie",
            "rating": 7,
        }
        response = self.client.post(self.url, data=json_data, format="json")
        result = {"id": 4, "text": "Exciting Movie", "rating": 7, "movie_id": 1}

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], 4)
        self.assertEqual(response.data, result)

    @pytestmark
    def test_put_review(self):
        url = f"{self.url}1/"
        json_data = {
            "text": "Exciting Movie",
            "rating": 7,
        }
        response = self.client.put(url, data=json_data, format="json")
        result = {"id": 1, "text": "Exciting Movie", "rating": 7, "vote": 0}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        response.data.pop("created_at")
        response.data.pop("updated_at")
        self.assertEqual(response.data, result)

    @pytestmark
    def test_patch_review(self):
        url = f"{self.url}3/"
        json_data = {
            "text": "Exciting Movie",
        }
        response = self.client.patch(url, data=json_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Exciting Movie")

    @pytestmark
    def test_delete_review_detail(self):
        url = f"{self.url}3/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestReviewVoteView(APITestCase):
    @pytestmark
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/v1/reviews/vote/"
        self.review_one = baker.make(Review)
        self.review_two = baker.make(Review)
        self.review_three = baker.make(Review)
        self.review_vote_one = baker.make(ReviewVote, review_id=self.review_one)
        self.review_vote_two = baker.make(ReviewVote, review_id=self.review_one)
        self.review_vote_three = baker.make(ReviewVote, review_id=self.review_one)

    @pytestmark
    def test_post_review_vote(self):
        json_data = {
            "review_id": 1,
        }
        self.assertEqual(self.review_one.vote, 3)

        response = self.client.post(self.url, data=json_data, format="json")
        result = {"review_id": 1}

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, result)
        self.assertEqual(self.review_one.vote, 4)

    @pytestmark
    def test_delete_review_vote(self):
        url = f"{self.url}3/"
        self.assertEqual(self.review_one.vote, 3)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.review_one.vote, 2)
