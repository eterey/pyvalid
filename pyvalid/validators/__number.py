from sys import version_info
try:
    from collections.abc import Iterable, Container
except ImportError:
    from collections import Iterable, Container

from pyvalid import accepts
from pyvalid.validators import AbstractValidator


class NumberValidator(AbstractValidator):

    number_types = (int, float)
    if version_info < (3, 0, 0):
        number_types += (long, )  # noqa: F821

    @classmethod
    def min_val_checker(cls, val, min_val):
        return val >= min_val

    @classmethod
    def max_val_checker(cls, val, max_val):
        return val <= max_val

    @classmethod
    def in_range_checker(cls, val, in_range):
        is_valid = False
        if isinstance(in_range, Container):
            is_valid = val in in_range
        elif isinstance(in_range, Iterable):
            for item in in_range:
                if item == val:
                    is_valid = True
                    break
        return is_valid

    @classmethod
    def not_in_range_checker(cls, val, not_in_range):
        return not cls.in_range_checker(val, not_in_range)

    @property
    def checkers(self):
        return self.__checkers

    @accepts(
        object, min_val=number_types, max_val=number_types,
        in_range=[Iterable, Container], not_in_range=[Iterable, Container]
    )
    def __init__(self, **kwargs):
        self.__checkers = {
            NumberValidator.min_val_checker: [kwargs.get('min_val', None)],
            NumberValidator.max_val_checker: [kwargs.get('max_val', None)],
            NumberValidator.in_range_checker: [kwargs.get('in_range', None)],
            NumberValidator.not_in_range_checker: [kwargs.get('not_in_range', None)]
        }
        AbstractValidator.__init__(self)

    def __call__(self, val):
        valid = isinstance(val, NumberValidator.number_types) and self._check(val)
        return valid
