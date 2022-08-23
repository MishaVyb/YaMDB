from django.db.models import Avg
from rest_framework import viewsets

from api.permissions import (
    IsAdminOrReadOnly, IsAuthorOrReadOnly
)
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleGetSerializer,
    TitlePostSerializer,
)
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    ordering_fields = ('year', 'name')
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleGetSerializer
        return TitlePostSerializer
