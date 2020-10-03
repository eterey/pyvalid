from types import MethodType
from pyvalid.__exceptions import InvalidReturnTypeError
from pyvalid.switch import is_enabled
from functools import wraps
try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable


class Returns(Callable):
    """A decorator to validate the returns value of a given function.
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
