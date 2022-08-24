from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet
from django.urls import include, path

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
