from django.urls import path

from reviews.views import ReviewDetailView, ReviewCreateUpdateDeleteView, ReviewVoteCreateView, ReviewVoteDeleteView

app_name = "reviews"

urlpatterns = [
    path("", ReviewCreateUpdateDeleteView.as_view()),
    path("<int:pk>/", ReviewDetailView.as_view()),
    path("vote/", ReviewVoteCreateView.as_view()),
    path("vote/<int:pk>/", ReviewVoteDeleteView.as_view()),
]
