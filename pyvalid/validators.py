import sys
import re
from abc import ABCMeta, abstractmethod
from pyvalid import accepts
from six import with_metaclass
try:
    from collections.abc import Iterable, Container, Callable
except ImportError:
    from collections import Iterable, Container, Callable


class Validator(Callable):

    @accepts(object, Callable)
    def __init__(self, func):
        self.__func = func

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)


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
            except (IndexError, TypeError):
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


class IterableValidator(AbstractValidator):
    """
    This class performs validation on the content of the iterable to check if the given iterable is valid or not.
    The iterable can be either a list, tuple or even keys or values of a dictionary.

    Example usage:
        @accepts(IterableValidator(empty_allowed=False, elements_type=int, min_val=0, max_val=50))
        def example([1, 3, 7, 10]):
            pass
    """

    iterable_types = (list, tuple, dict, set)

    @classmethod
    def empty_iterable_checker(cls, val, empty_allowed):
        """
        Check if the iterable is empty or not.

        Args:
            val (list/tuple/dict/set): Iterable to be validated.
            empty_allowed (bool): If this flag is set to 'True', this method raises exception and terminates the
                                  execution if the iterable is empty.
                                  If set to 'False', it raises a warning and continues with the execution.

        Returns (bool):
            True: If the iterable is not empty.
            False: If the iterable is empty.
        """
        if not empty_allowed:
            return len(val) != 0
        else:
            if len(val) == 0:
                print("WARNING! Iterable is empty, but does not impact the execution.")
            return True

    @classmethod
    def element_type_checker(cls, val, elements_type):
        """
        Checks if all the elements of the iterable are of required type.

        Args:
            val (list/tuple/dict/set): Iterable whose contents needs to be validated.
            elements_type (datatype): Expected type of all the elements in the iterator.

        Returns (bool):
            True: If all elements of the iterable are of required type.
            False: If at least one element of the iterable is not of required type.
        """
        valid = False
        for element in val:
            valid = isinstance(element, elements_type)
            if not valid:
                break

        return valid

    @classmethod
    def elements_min_val_checker(cls, val, min_val):
        """
        Checks if all the elements of the iterable are greater than or equal to the specified value.

        Args:
            val (list/tuple/dict/set): Iterable whose contents needs to be validated.
            min_val (int): Expected minimum value the iterable must contain.

        Returns (bool):
            True: If all the elements of the iterable are greater than or equal to the <min_val>.
            False: If at least one element of the iterable is less than the <min_val>.
        """
        valid = True

        for element in val:
            if element < min_val:
                valid = False
                break

        return valid

    @classmethod
    def elements_max_val_checker(cls, val, max_val):
        """
        Checks if all the elements of the iterable are less than or equal to the specified value.

        Args:
            val (list/tuple/dict/set): Iterable whose contents needs to be validated.
            max_val (int): Expected maximum value the iterable must contain.

        Returns (bool):
            True: If all the elements of the iterable are less than or equal to the <max_val>.
            False: If at least one element of the iterable is greater than the <max_val>.
        """
        valid = True

        for element in val:
            if element > max_val:
                valid = False
                break

        return valid

    @property
    def checkers(self):
        return self.__checkers

    @accepts(object, empty_allowed=bool, element_type=(str, int, float), min_val=(int, float), max_val=(int, float))
    def __init__(self, **kwargs):
        self.__checkers = {
            IterableValidator.empty_iterable_checker: [kwargs.get('empty_allowed', None)],
            IterableValidator.element_type_checker: [kwargs.get('elements_type', None)],
            IterableValidator.elements_min_val_checker: [kwargs.get('min_val', None)],
            IterableValidator.elements_max_val_checker: [kwargs.get('max_val', None)]
        }
        AbstractValidator.__init__(self)

    def __call__(self, val):
        valid = isinstance(val, IterableValidator.iterable_types) and self._check(val)
        return valid


is_validator = Validator


__all__ = [
    'is_validator',
    'Validator',
    'NumberValidator',
    'StringValidator',
    'IterableValidator'
]
