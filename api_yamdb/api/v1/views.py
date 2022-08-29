from api.v1.filters import TitleFilter
from api.v1.permissions import (IsAdminOrReadOnlyPermission,
                                IsAuthorAdminModeratorOrReadOnly)
from api.v1.serializers import (CategorySerializer, CommentSerializer,
                                GenreSerializer, ReviewSerializer,
                                TitleGetSerializer, TitlePostSerializer)
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Title


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnlyPermission]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyPermission]
    pagination_class = PageNumberPagination
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer

    # def get_queryset(self):
    #     queryset = Title.objects.annotate(
    #         rating=Avg('reviews__score')).order_by('name')

    #     category = self.request.query_params.get('category', None)
    #     if category is not None:
    #         queryset = queryset.filter(category__slug=category)

    #     genre = self.request.query_params.get('genre', None)
    #     if genre is not None:
    #         queryset = queryset.filter(genre__slug=genre)

    #     name = self.request.query_params.get('name', None)
    #     if name is not None:
    #         queryset = queryset.filter(name__icontains=name)

    #     year = self.request.query_params.get('year', None)
    #     if year is not None:
    #         queryset = queryset.filter(year=year)

    #     return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly,
    )
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
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly,
    )
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
