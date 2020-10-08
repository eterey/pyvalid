import re
try:
    from collections.abc import Iterable, Container
except ImportError:
    from collections import Iterable, Container

from pyvalid import accepts
from pyvalid.validators import AbstractValidator


class StringValidator(AbstractValidator):

    @classmethod
    def min_len_checker(cls, val, min_len):
        return len(val) >= min_len

    @classmethod
    def max_len_checker(cls, val, max_len):
        return len(val) <= max_len

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

    @classmethod
    def re_checker(cls, val, pattern, flags=0):
        try:
            match_obj = re.match(pattern, val, flags)
            is_valid = match_obj is not None
        except re.error:
            is_valid = False
        return is_valid

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
        AbstractValidator.__init__(self)

    def __call__(self, val):
        valid = isinstance(val, str) and self._check(val)
        return valid
