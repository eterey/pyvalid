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
        min_val = kwargs.get('min_val', None)
        max_val = kwargs.get('max_val', None)
        if min_val is not None and max_val is not None and min_val > max_val:
            raise ValueError('Min value can\'t be greater than max value!')
        in_range = kwargs.get('in_range', None)
        not_in_range = kwargs.get('not_in_range', None)
        self.__checkers = {
            NumberValidator.min_val_checker: [min_val],
            NumberValidator.max_val_checker: [max_val],
            NumberValidator.in_range_checker: [in_range],
            NumberValidator.not_in_range_checker: [not_in_range]
        }
        AbstractValidator.__init__(self, allowed_types=NumberValidator.number_types)
