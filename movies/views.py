from django.db.models import Avg
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from movies.models import Genre, Movie
from movies.serializers import MovieDetailSerializer, MovieSerializer


class MovieListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Movie.objects.all()
    permision_classes = [AllowAny]
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        genres = request.data.pop("genres")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, genres)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, genres):
        _genres = []
        for genre in genres:
            _genre, _ = Genre.objects.get_or_create(name=genre)
            _genres.append(_genre.id)
        serializer.save(genres=_genres)

    def filter_queryset(self, queryset):
        # get query parms
        title = self.request.query_params.get("title")
        year = self.request.query_params.get("year")
        genres = self.request.query_params.get("genres")
        order = self.request.query_params.get("order")
        filter_kwargs = {}
        if title is not None:
            filter_kwargs["title__icontains"] = title
        if year is not None and len(year) == 4:
            filter_kwargs["year"] = year
        if genres is not None:
            genre = Genre.objects.get(name=genres)
            filter_kwargs["genres"] = genre

        queryset = queryset.filter(**filter_kwargs)

        if order == "ascending":
            queryset = queryset.annotate(avg_rate=Avg("reviews__rating")).order_by(
                "avg_rate"
            )
        if order == "descending":
            queryset = queryset.annotate(avg_rate=Avg("reviews__rating")).order_by(
                "-avg_rate"
            )
        return super().filter_queryset(queryset)


class MovieView(RetrieveAPIView):
    queryset = Movie.objects.all()
    permision_classes = [AllowAny]
    serializer_class = MovieDetailSerializer
