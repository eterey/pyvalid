import sys
from abc import ABCMeta, abstractmethod
from pyvalid import accepts
from collections import Iterable, Container
from six import with_metaclass


class Validator(with_metaclass(ABCMeta)):

    @property
    @abstractmethod
    def checkers(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def settings(self):
        raise NotImplementedError

    @settings.setter
    @abstractmethod
    def settings(self, value):
        raise NotImplementedError

    @abstractmethod
    def __call__(self, val):
        raise NotImplementedError

    def __init__(self):
        for key, val in list(self.settings.items()):
            if (key not in self.checkers) or (val is None):
                del self.settings[key]

    def _check(self, val):
        valid = True
        for checker_name, checker_arg in self.settings.items():
            checker = self.checkers[checker_name]
            valid = checker(val, checker_arg)
            if not valid:
                break
        return valid


class NumberValidator(Validator):

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
    def settings(self):
        return self.__settings

    @settings.setter
    def settings(self, value):
        self.__settings = value

    @property
    def checkers(self):
        return self.__checkers

    @accepts(
        object, min_val=number_types, max_val=number_types,
        in_range=[Iterable, Container], not_in_range=[Iterable, Container]
    )
    def __init__(self, **kwargs):
        self.__settings = kwargs
        self.__checkers = {
            'min_val': NumberValidator.min_val_checker,
            'max_val': NumberValidator.max_val_checker,
            'in_range': NumberValidator.in_range_checker,
            'not_in_range': NumberValidator.not_in_range_checker
        }
        Validator.__init__(self)

    def __call__(self, val):
        valid = isinstance(val, NumberValidator.number_types) and \
            self._check(val)
        return valid


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

    @property
    def settings(self):
        return self.__settings

    @settings.setter
    def settings(self, value):
        self.__settings = value

    @property
    def checkers(self):
        return self.__checkers

    @accepts(
        object, min_len=int, max_len=int,
        in_range=[Iterable, Container], not_in_range=[Iterable, Container]
    )
    def __init__(self, **kwargs):
        self.__settings = kwargs
        self.__checkers = {
            'min_len': StringValidator.min_len_checker,
            'max_len': StringValidator.max_len_checker,
            'in_range': StringValidator.in_range_checker,
            'not_in_range': StringValidator.not_in_range_checker
        }
        Validator.__init__(self)

    def __call__(self, val):
        valid = isinstance(val, str) and self._check(val)
        return valid
