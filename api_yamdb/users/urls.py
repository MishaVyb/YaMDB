from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import (ConfirmationCodeTokenView, SelfUserView, SignUpView,
                         UsersViewSet)

router = DefaultRouter()
router.register('users', UsersViewSet)

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', ConfirmationCodeTokenView.as_view(), name='token'),
    path('users/me/', SelfUserView.as_view(), name='me'),
    path('', include(router.urls)),
]
