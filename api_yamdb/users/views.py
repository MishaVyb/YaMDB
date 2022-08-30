import random

from api.v1.permissions import AdminOnlyPermission
from api.v1.serializers import (ConfirmationCodeTokenSerializer,
                                SelfUserSerializer, UserSerializer)
from django.core.mail import send_mail
from rest_framework import generics, pagination, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Confirmation, User

from api_yamdb.settings import DIGITS_AMOUNT_AT_CONFIRMATION_CODE


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    email_from = 'no-reply@yamdb.ru'
    email_subject = 'Confirmation code'
    email_message = (
        'Привет, {username}! Регистрация на YaMDB успешна выполнена. '
        'Твой код подтверждения для входа: {code}. '
    )

    def generate_code(self, user: User) -> int:
        start = 1
        end = (10**DIGITS_AMOUNT_AT_CONFIRMATION_CODE) - 1
        confirmation_code = random.randint(start, end)

        Confirmation.objects.create(
            username=user.username, code=confirmation_code
        )
        return confirmation_code

    def send_confirmation_code(self, user: User, code: int):
        send_mail(
            subject=self.email_subject,
            message=self.email_message.format(
                username=user.username, code=code
            ),
            recipient_list=[user.email],
            from_email=self.email_from,
        )

    def post(self, request: Request):
        response = super().post(request)

        user: User = User.objects.get(username=response.data['username'])
        code = self.generate_code(user)
        self.send_confirmation_code(user, code)

        data = {
            'username': response.data['username'],
            'email': response.data['email'],
        }
        return Response(data, status=status.HTTP_200_OK)


class ConfirmationCodeTokenView(TokenObtainPairView):
    serializer_class = ConfirmationCodeTokenSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnlyPermission]
    pagination_class = pagination.PageNumberPagination
    lookup_field = 'username'


class SelfUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SelfUserSerializer

    def get_object(self):
        return self.request.user
