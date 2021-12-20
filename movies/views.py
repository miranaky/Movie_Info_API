from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny


from movies.models import Movie, Genre

from movies.serializers import MovieSerializer, MovieDetailSerializer


class MovieListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Movie.objects.all()
    permision_classes = [AllowAny]
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        # get query parms
        title = self.request.query_params.get("title")
        rating = self.request.query_params.get("rating")
        year = self.request.query_params.get("year")
        genres = self.request.query_params.get("genres")
        filter_kwargs = {}
        if title is not None:
            filter_kwargs["title__icontains"] = title
        if year is not None and len(year) == 4:
            filter_kwargs["year"] = year
        if genres is not None:
            genre = Genre.objects.get(name=genres)
            filter_kwargs["genres"] = genre

        queryset = queryset.filter(**filter_kwargs)
        # if rating == "ascending":
        #     queryset = queryset.annotate(ordering=F("rating")).order_by("ordering")
        # if rating == "descending":
        #     queryset = queryset.annotate(ordering=F("rating")).order_by("-ordering")
        return super().filter_queryset(queryset)


class MovieView(RetrieveAPIView):
    queryset = Movie.objects.all()
    permision_classes = [AllowAny]
    serializer_class = MovieDetailSerializer
