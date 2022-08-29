class Constant(object):
    def __init__(self, value):
        self._value = value

    def __set__(self, instance, value):
        raise NotImplementedError('Assign to a constant value is forbidden.')

    def __get__(self, instance, cls=None):
        return self._value

    def __delete__(self, obj) -> None:
        raise NotImplementedError('Dellete a constant value is forbidden.')
