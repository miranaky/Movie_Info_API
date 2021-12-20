from django.urls import path

from movies.views import MovieListView, MovieView

app_name = "movies"

urlpatterns = [
    path("", MovieListView.as_view()),
    path("<int:pk>/", MovieView.as_view()),
]
