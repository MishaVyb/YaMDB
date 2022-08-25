from rest_framework.request import Request
from users.exeptions import InvalidConfirmationCode, NoneConfirmationCode
from users.models import User, Confirmation
from django.shortcuts import get_object_or_404


class ConfirmationCodeBackend:
    def authenticate(self, request: Request,
                     username: str,
                     confirmation_code: int):
        user = get_object_or_404(User, username=username)
        if not hasattr(user, 'confirmation'):
            raise NoneConfirmationCode

        if not user.confirmation.code == confirmation_code:
            raise InvalidConfirmationCode

        Confirmation.objects.filter(user=user).delete()

        return user
