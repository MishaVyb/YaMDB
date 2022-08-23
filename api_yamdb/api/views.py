from django.shortcuts import get_object_or_404
from reviews.models import Title, Review
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .permissions import ReviewCommentPermission
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (ReviewCommentPermission,)
    pagination_class = PageNumberPagination

    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(title=title, author=self.request.user)

    def get_queryset(self):
        title = get_object_or_404(Title,
                                  pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (ReviewCommentPermission,)
    pagination_class = PageNumberPagination

    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(review=review, author=self.request.user)

    def get_queryset(self):
        title = get_object_or_404(Title,
                                  pk=self.kwargs.get('title_id'))
        review = get_object_or_404(title.reviews.all(),
                                   pk=self.kwargs.get('review_id'))
        return review.comments.all()
