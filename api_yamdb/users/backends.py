from typing import Union

from rest_framework.request import Request
from users.exeptions import InvalidConfirmationCode, NoneConfirmationCode
from users.models import User, Confirmation
from django.shortcuts import get_object_or_404


class ConfirmationCodeBackend:
    def authenticate(
        self, request: Request, username: str, confirmation_code: int
        ):
        user = get_object_or_404(User, username=username)
        try:
            confirmation = Confirmation.objects.get(username=username)
        except:
            raise NoneConfirmationCode

        Confirmation.object.filter(username=username).delete()
        if not confirmation.code == confirmation_code:
            raise InvalidConfirmationCode
        return user
