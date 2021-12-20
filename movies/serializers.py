from rest_framework.serializers import ModelSerializer, StringRelatedField

from movies.models import Movie
from reviews.serializers import ReviewSerializer


class MovieSerializer(ModelSerializer):
    genres = StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = ("id", "title", "year", "rating", "genres", "summary")
        read_only_fields = (
            "id",
            "rating",
        )
