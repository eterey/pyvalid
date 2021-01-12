import re
try:
    from collections.abc import Iterable, Container
except ImportError:
    from collections import Iterable, Container

from pyvalid import accepts
from pyvalid.validators import AbstractValidator, IsValid


class StringValidator(AbstractValidator):

    @classmethod
    def min_len_checker(cls, val, min_len):
        IsValid.status = len(val) >= min_len
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"expected string length to be '<={min_len}' but got length '{val}' instead."

        return IsValid

    @classmethod
    def max_len_checker(cls, val, max_len):
        IsValid.status = len(val) <= max_len
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"expected string length to be '>={max_len}' but got length '{val}' instead."

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

    @classmethod
    def re_checker(cls, val, pattern, flags=0):
        try:
            match_obj = re.match(pattern, val, flags)
            IsValid.status = match_obj is not None
        except re.error:
            IsValid.status = False
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"'{val}' must not match the pattern '{pattern}'."

        return IsValid

    @property
    def checkers(self):
        return self.__checkers

    @accepts(
        object, min_len=int, max_len=int,
        in_range=[Iterable, Container], not_in_range=[Iterable, Container],
        re_pattern=str, re_flags=int
    )
    def __init__(self, **kwargs):
        self.__checkers = {
            StringValidator.min_len_checker: [kwargs.get('min_len', None)],
            StringValidator.max_len_checker: [kwargs.get('max_len', None)],
            StringValidator.in_range_checker: [kwargs.get('in_range', None)],
            StringValidator.not_in_range_checker: [kwargs.get('not_in_range', None)],
            StringValidator.re_checker: [
                kwargs.get('re_pattern', None), kwargs.get('re_flags', 0)
            ]
        }
        AbstractValidator.__init__(self, allowed_types=str)
