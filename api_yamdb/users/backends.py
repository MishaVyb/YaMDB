from rest_framework.request import Request
from users.exeptions import InvalidConfirmationCode, NoneConfirmationCode
from users.models import Confirmation, User


class ConfirmationCodeBackend:

    def authenticate(
        self, request: Request, username: str, confirmation_code: int
    ):
        # в случае отсутсвие данного юзера, в валидаторе уже перехватывается и
        # обрабатывается исключение User.DoesNotExist, так что нет
        # необходимости в get_object_or_404
        user = User.objects.get(username=username)
        try:
            confirmation: Confirmation = Confirmation.objects.get(
                username=username
            )
        except Confirmation.DoesNotExist:
            raise NoneConfirmationCode
        if not confirmation.code == confirmation_code:
            raise InvalidConfirmationCode

        confirmation.delete()

        return user
