import sys
from abc import ABCMeta, abstractmethod
from pyvalid import accepts
from collections import Iterable, Container


if sys.version_info >= (3, 0, 0):
    class Validator(metaclass=ABCMeta):
        @abstractmethod
        def __call__(self, val):
            pass
else:
    class Validator(object):
        __metaclass__ = ABCMeta

        @abstractmethod
        def __call__(self, val):
            pass


class StringValidator(Validator):

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



    @accepts(
        object,
        min_len=int, max_len=int,
        in_range=[Iterable, Container], not_in_range=[Iterable, Container]
    )
    def __init__(self, **kwargs):
        self._checkers = {
            'min_len': StringValidator.min_len_checker,
            'max_len': StringValidator.max_len_checker,
            'in_range': StringValidator.in_range_checker,
            'not_in_range': StringValidator.not_in_range_checker
        }
        for key, val in list(kwargs.items()):
            if (key not in self._checkers) or (val is None):
                del kwargs[key]
        self.__checkers = kwargs

    def __call__(self, val):
        if isinstance(val, str):
            valid = True
            for checker_name, checker_arg in self.__checkers.items():
                checker = self._checkers[checker_name]
                valid = checker(val, checker_arg)
                if not valid:
                    break
        else:
            valid = False
        return valid
