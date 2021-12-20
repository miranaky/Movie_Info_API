from django.contrib import admin

from reviews.models import Review, ReviewVote


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """"""


@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    """"""
