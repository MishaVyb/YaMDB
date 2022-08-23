from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet


router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')