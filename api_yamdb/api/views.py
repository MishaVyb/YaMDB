from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.permissions import (
    AdminOnlyPermission, AdminOrReadOnlyPermission, AuthorAdminModeratorPermission
)
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleGetSerializer,
    TitlePostSerializer,
)
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    ordering_fields = ('year', 'name')
    permission_classes = (AdminOrReadOnlyPermission,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleGetSerializer
        return TitlePostSerializer
