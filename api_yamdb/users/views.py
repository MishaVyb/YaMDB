import random

from django.core.mail import send_mail
from rest_framework import generics, pagination, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.permitions import AdminUserPermission
from users.serializers import (ConfirmationCodeTokenSerializer,
                               SelfUserSerializer, UserSerializer)

from api_yamdb.settings import DIGITS_AMOUNT_AT_CONFIRMATION_CODE


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    email_from = 'no-reply@yamdb.ru'
    email_subject = 'Confirmation code'
    email_message = (
        'Hi, {username}! Registration for YaMDB completed successfully. '
        'Your confirmation code to login is: {code}. '
    )

    def generate_code(self, user: User):
        start = 1
        end = (10**DIGITS_AMOUNT_AT_CONFIRMATION_CODE) - 1
        user.confirmation_code = random.randint(start, end)
        user.save()

    def send_email(self, user: User):
        send_mail(
            subject=self.email_subject,
            message=self.email_message.format(
                username=user.username, code=user.confirmation_code
            ),
            recipient_list=[user.email],
            from_email=self.email_from,
        )

    def post(self, request: Request):
        response = super().post(request)

        user: User = User.objects.get(username=response.data['username'])
        self.generate_code(user)
        self.send_email(user)

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
    permission_classes = [AdminUserPermission]
    pagination_class = pagination.PageNumberPagination
    lookup_field = 'username'


class SelfUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SelfUserSerializer

    def get_object(self):
        return self.request.user
