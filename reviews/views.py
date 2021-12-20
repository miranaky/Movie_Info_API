from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny

from reviews.models import Review, ReviewVote
from reviews.serializers import (
    ReviewSerializer,
    ReviewVoteSerializer,
    ReviewWriteSerializer,
)


class ReviewDetailView(
    RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericAPIView
):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_class = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ReviewCreateUpdateDeleteView(CreateModelMixin, GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewWriteSerializer
    permission_class = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReviewVoteCreateView(CreateAPIView):
    queryset = ReviewVote.objects.all()
    serializer_class = ReviewVoteSerializer
    permission_class = [AllowAny]


class ReviewVoteDeleteView(DestroyAPIView):
    queryset = ReviewVote.objects.all()
    serializer_class = ReviewVoteSerializer
    permission_class = [AllowAny]
