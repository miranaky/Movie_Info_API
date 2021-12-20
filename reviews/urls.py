from django.urls import path

from reviews.views import ReviewDetailView, ReviewCreateUpdateDeleteView

app_name = "reviews"

urlpatterns = [
    path("", ReviewCreateUpdateDeleteView.as_view()),
    path("<int:pk>/", ReviewDetailView.as_view()),
]
