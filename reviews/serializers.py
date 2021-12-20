from rest_framework.serializers import ModelSerializer

from reviews.models import Review, ReviewVote


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "rating",
            "created_at",
            "updated_at",
            "vote",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "vote",
        )


class ReviewWriteSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "rating",
            "movie_id",
        )


class ReviewVoteSerializer(ModelSerializer):
    class Meta:
        model = ReviewVote
        fields = ("review_id",)
