from django.shortcuts import get_object_or_404
from reviews.models import Review, Comment
from rest_framework import viewsets, permissions, mixins, filters
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorAllOthersReadOnly
from .serializers import (CommentSerializer, ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorAllOthersReadOnly,)

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorAllOthersReadOnly,)

    queryset = Comment.objects.all()
    serializer_class = ReviewSerializer
    # pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
