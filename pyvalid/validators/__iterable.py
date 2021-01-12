try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

from pyvalid import accepts
from pyvalid.validators import AbstractValidator, IsValid


class IterableValidator(AbstractValidator):
    """This class performs validation on the content of the iterable to check if the
    given iterable is valid or not. The iterable can be either a list, tuple or even
    keys or values of a dictionary.

    Example:

    .. code-block:: python

        validator = IterableValidator(
            empty_allowed=False, elements_type=int, min_val=0, max_val=50
        )
        @accepts(validator)
        def example([1, 3, 7, 10]):
            pass

    """

    @classmethod
    def iterable_type_checker(cls, val, iterable_type):
        """Checks if the iterable is of required data type.

        Args:
            val (Iterable):
                Tensor whose type is to be validated.
            iterable_type (type):
                Expected data type of iterable.
                Ex: list, tuple, dict.

        Returns (bool):
            True:
                If the type of given iterable matches the required type.
            False:
                If the type of given iterable does not match the required type.

        """
        IsValid.status = type(val) == iterable_type
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"expected type '{iterable_type}' but got '{type(val)}' instead."

        return IsValid

    @classmethod
    def empty_checker(cls, val, empty_allowed):
        """Checks if the iterable is empty or not.

        Args:
            val (collections.abc.Iterable):
                Iterable whose contents needs to be validated.
            empty_allowed (bool):
                If this flag is set to ``False``, this method raises exception and
                terminates the execution if the iterable is empty.
                If set to ``True``, it raises a warning and continues with
                the execution.

        Returns (bool):
            True:
                If the iterable is not empty.
            False:
                If the iterable is empty.
        """
        if not empty_allowed:
            IsValid.status = len(val) != 0
            if not IsValid.status:
                IsValid.msg = f"In {IsValid.get_caller()}, " \
                              f"expected non-empty iterable but got '{val}"
        else:
            IsValid.status = True
            IsValid.is_warning = True
            IsValid.msg = "In {IsValid.get_caller()}, iterable is empty."

        return IsValid

    @classmethod
    def element_type_checker(cls, val, elements_type):
        """Checks if all the elements of the iterable are of required type.

        Args:
            val (collections.abc.Iterable):
                Iterable whose contents needs to be validated.
            elements_type (datatype):
                Expected type of all the elements in the iterator.

        Returns (bool):
            True:
                If all elements of the iterable are of required type.
            False:
                If at least one element of the iterable is not of required type.
        """
        IsValid.status = True
        for element in val:
            IsValid.status = isinstance(element, elements_type)
            if not IsValid.status:
                IsValid.msg = f"In {IsValid.get_caller()}, " \
                              f"expected type '{elements_type}' but got '{type(element)}' instead."
                break

        return IsValid

    @classmethod
    def elements_min_val_checker(cls, val, min_val):
        """Checks if all the elements of the iterable are greater than or equal to the
        specified value.

        Args:
            val (collections.abc.Iterable):
                Iterable whose contents needs to be validated.
            min_val (int):
                Expected minimum value the iterable must contain.

        Returns (bool):
            True:
                If all the elements of the iterable are greater than or equal to the
                <min_val>.
            False:
                If at least one element of the iterable is less than the
                <min_val>.
        """
        IsValid.status = True
        for element in val:
            if element < min_val:
                IsValid.status = False
                IsValid.msg = f"In {IsValid.get_caller()}, " \
                              f"expected '>={min_val}' but got '{val}' instead."
                break

        return IsValid

    @classmethod
    def elements_max_val_checker(cls, val, max_val):
        """Checks if all the elements of the iterable are less than or equal to the
        specified value.

        Args:
            val (collections.abc.Iterable):
                Iterable whose contents needs to be validated.
            max_val (int):
                Expected maximum value the iterable must contain.

        Returns (bool):
            True:
                If all the elements of the iterable are less than or equal to the
                <max_val>.
            False:
                If at least one element of the iterable is greater than the
                <max_val>.
        """
        IsValid.status = True
        for element in val:
            if element > max_val:
                IsValid.status = False
                IsValid.msg = f"In {IsValid.get_caller()}, " \
                              f"expected '<={max_val}' but got '{val}' instead."
                break

        return IsValid

    @property
    def checkers(self):
        return self.__checkers

    @accepts(object, empty_allowed=bool, element_type=(str, int, float),
             min_val=(int, float), max_val=(int, float))
    def __init__(self, **kwargs):
        min_val = kwargs.get('min_val', None)
        max_val = kwargs.get('max_val', None)
        if min_val is not None and max_val is not None and min_val > max_val:
            raise ValueError('Min value can\'t be greater than max value!')
        iterable_type = kwargs.get('iterable_type', None)
        empty_allowed = kwargs.get('empty_allowed', None)
        elements_type = kwargs.get('elements_type', None)

        self.__checkers = {
            IterableValidator.empty_checker: [empty_allowed],
            IterableValidator.element_type_checker: [elements_type],
            IterableValidator.iterable_type_checker: [iterable_type],
            IterableValidator.elements_min_val_checker: [min_val],
            IterableValidator.elements_max_val_checker: [max_val]
        }
        AbstractValidator.__init__(self, allowed_types=Iterable)
