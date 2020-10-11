from functools import wraps
from types import MethodType
try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable

from pyvalid.__exceptions import InvalidReturnTypeError
from pyvalid.switch import is_enabled


class Returns(Callable):
    """
    ``pyvalid.returns(*allowed_return_values)``
    +++++++++++++++++++++++++++++++++++++++++++

    The decorator which validates the value returned by the wrapped function.

    To use it, we need to specify the list of expected return types or values. If the
    function’s return value doesn’t match the allowed types/values, the
    ``pyvalid.InvalidReturnTypeError`` error will be thrown.

    Examples of usage:

    Let's define the ``multiply`` function, which returns only ``int`` values, and see
    how does it work with other types.

    .. code-block:: python

        from pyvalid import returns


        @returns(int)
        def multiply(num_1, num_2):
            return num_1 * num_2


        multiply(4, 2)
        # Returns 8.

        multiply(3.14, 8)
        # Raises the InvalidReturnTypeError exception, since the function returns the
        # float value, when we're expecting int values only.

        multiply(3, 'pyvalid')
        # Raises the InvalidReturnTypeError exception, since the function returns the
        # str value, when we're expecting int values only.
    """

    def __init__(self, *allowed_return_values):
        self.allowed_return_values = allowed_return_values

    def __call__(self, func):
        @wraps(func)
        def decorator_wrapper(*func_args, **func_kwargs):
            from pyvalid.validators import Validator
            returns_val = func(*func_args, **func_kwargs)
            if is_enabled() and self.allowed_return_values:
                is_valid = False
                for allowed_val in self.allowed_return_values:
                    if isinstance(allowed_val, (Validator, MethodType)):
                        if isinstance(allowed_val, Validator):
                            is_valid = allowed_val(returns_val)
                        elif (isinstance(allowed_val, MethodType) and
                                hasattr(allowed_val, '__func__') and
                                isinstance(allowed_val.__func__, Validator)):
                            is_valid = allowed_val(returns_val)
                    elif isinstance(allowed_val, type):
                        is_valid = isinstance(
                            returns_val, allowed_val
                        )
                    else:
                        is_valid = returns_val == allowed_val
                    if is_valid:
                        break
                if not is_valid:
                    raise InvalidReturnTypeError(
                        func, returns_val, self.allowed_return_values
                    )
            return returns_val
        return decorator_wrapper
