from typing import Union

from rest_framework.request import Request
from users.exeptions import InvalidConfirmationCode, NoneConfirmationCode
from users.models import User


class ConfirmationCodeBackend:
    def authenticate(
        self, request: Request, username: str, confirmation_code: int
    ):
        user = self.get_user(username)
        if not hasattr(user, 'confirmation_code'):
            raise RuntimeError(
                'Update your custom User model with `confirmation_code` field.'
            )
        if user.confirmation_code is None:
            return NoneConfirmationCode
        if not user.confirmation_code == confirmation_code:
            raise InvalidConfirmationCode
        return user

    def get_user(self, user_id: Union[str, int]) -> User:
        if isinstance(user_id, str):
            return User.objects.get(username=user_id)
        elif isinstance(user_id, int):
            return User.objects.get(pk=user_id)
        raise TypeError
