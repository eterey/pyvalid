from sys import version_info
try:
    from collections.abc import Iterable, Container
except ImportError:
    from collections import Iterable, Container

from pyvalid import accepts
from pyvalid.validators import AbstractValidator, IsValid


class NumberValidator(AbstractValidator):

    number_types = (int, float)
    if version_info < (3, 0, 0):
        number_types += (long, )  # noqa: F821

    @classmethod
    def number_type_checker(cls, val, number_type):
        """Checks if the number is of required data type.

        Args:
            val (number):
                Tensor whose type is to be validated.
            number_type (type):
                Expected data type of number.
                Ex: int, float, long.

        Returns (bool):
            True:
                If the type of given number matches the required type.
            False:
                If the type of given number does not match the required type.

        """
        IsValid.status = type(val) == number_type
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"expected type '{number_type}' but got '{type(val)}' instead."

        return IsValid

    @classmethod
    def min_val_checker(cls, val, min_val):
        IsValid.status = val >= min_val
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"expected '>={min_val}' but got '{val}' instead."

        return IsValid

    @classmethod
    def max_val_checker(cls, val, max_val):
        IsValid.status = val <= max_val
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"expected '<={max_val}' but got '{val}' instead."

        return IsValid

    @classmethod
    def in_range_checker(cls, val, in_range):
        if isinstance(in_range, Container):
            IsValid.status = val in in_range
        elif isinstance(in_range, Iterable):
            for item in in_range:
                if item == val:
                    IsValid.status = True
                    break
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"'{val}' must be in range '{in_range}'."

        return IsValid

    @classmethod
    def not_in_range_checker(cls, val, not_in_range):
        in_range = cls.in_range_checker(val, not_in_range)
        IsValid.status = not in_range.status
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"'{val}' must not be in range '{not_in_range}'."

        return IsValid

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
        number_type = kwargs.get('number_type', None)
        in_range = kwargs.get('in_range', None)
        not_in_range = kwargs.get('not_in_range', None)

        self.__checkers = {
            NumberValidator.min_val_checker: [min_val],
            NumberValidator.max_val_checker: [max_val],
            NumberValidator.number_type_checker: [number_type],
            NumberValidator.in_range_checker: [in_range],
            NumberValidator.not_in_range_checker: [not_in_range]
        }
        AbstractValidator.__init__(self, allowed_types=NumberValidator.number_types)
