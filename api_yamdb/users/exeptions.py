class NoneConfirmationCode(Exception):
    message = (
        'User has not asked for confirmation code yet. '
        'Hint: request siqnup endpoint first. '
    )


class InvalidConfirmationCode(Exception):
    message = 'Invalid confirmation code'
