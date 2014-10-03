import sys
import re
from abc import ABCMeta, abstractmethod
from pyvalid import accepts
from collections import Iterable, Container, Callable, Sized
from six import with_metaclass


class Validator(Callable):

    @accepts(object, Callable)
    def __init__(self, func):
        self.__func = func

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)


def is_validator(func):
    return Validator(func)


class AbstractValidator(with_metaclass(ABCMeta, Validator)):

    @property
    @abstractmethod
    def checkers(self):
        raise NotImplementedError

    @abstractmethod
    def __call__(self, val):
        raise NotImplementedError

    def __init__(self):
        Validator.__init__(self, self)
        for checker_func, checker_args in list(self.checkers.items()):
            try:
                to_del = checker_args[0] is None
            except:
                to_del = True
            if to_del:
                del self.checkers[checker_func]

    def _check(self, val):
        valid = True
        for checker_func, checker_args in self.checkers.items():
            valid = checker_func(val, *checker_args)
            if not valid:
                break
        return valid


class NumberValidator(AbstractValidator):

    number_types = (int, float)
    if sys.version_info < (3, 0, 0):
        number_types += (long, )

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
            NumberValidator.not_in_range_checker: [
                kwargs.get('not_in_range', None)
            ]
        }
        AbstractValidator.__init__(self)

    def __call__(self, val):
        valid = isinstance(val, NumberValidator.number_types) and \
            self._check(val)
        return valid


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
            StringValidator.not_in_range_checker: [
                kwargs.get('not_in_range', None)
            ],
            StringValidator.re_checker: [
                kwargs.get('re_pattern', None), kwargs.get('re_flags', 0)
            ]
        }
        AbstractValidator.__init__(self)

    def __call__(self, val):
        valid = isinstance(val, str) and self._check(val)
        return valid


__all__ = [
    'is_validator',
    'Validator'
    'NumberValidator',
    'StringValidator'
]
