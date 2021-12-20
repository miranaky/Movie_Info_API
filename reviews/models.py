from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movie_id = models.ForeignKey("movies.Movie", related_name="reviews", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie_id}-{self.text}"


class ReviewVote(models.Model):
    review_id = models.ForeignKey("Review", related_name="review_vote", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.review_id.id)
