from django.contrib import admin

from movies.models import Genre, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Movie Admin Definition"""

    list_display = (
        "title",
        "year",
        "summary",
        "rating",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """"""
