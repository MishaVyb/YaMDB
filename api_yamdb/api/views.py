from django.db.models import Avg
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination

from api.permissions import (
    ListAnyOtherAdmin, GetAnyOtherAdmin
)

from api.serializers import (
    CategorySerializer, GenreSerializer, TitleGetSerializer,
    TitlePostSerializer,
)
from reviews.models import Category, Genre, Title
from django.shortcuts import get_object_or_404
from reviews.models import Title, Review

from .permissions import (ListAnyOtherAdmin,
                          GetAnyOtherAdmin,
                          ReviewCommentPermission)
from .serializers import CommentSerializer, ReviewSerializer


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ListAnyOtherAdmin]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ListAnyOtherAdmin]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [GetAnyOtherAdmin]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleGetSerializer
        return TitlePostSerializer

    def get_queryset(self):
        queryset = Title.objects.annotate(
            rating=Avg('reviews__score')).order_by('name')

        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__slug=category)

        genre = self.request.query_params.get('genre', None)
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(year=year)

        return queryset


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
