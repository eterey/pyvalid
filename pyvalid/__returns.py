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

    def __init__(self, *accepted_returns_values):
        self.accepted_returns_values = accepted_returns_values

    def __call__(self, func):
        @wraps(func)
        def decorator_wrapper(*func_args, **func_kwargs):
            from pyvalid.validators import Validator
            returns_val = func(*func_args, **func_kwargs)
            if is_enabled() and self.accepted_returns_values:
                is_valid = False
                for accepted_val in self.accepted_returns_values:
                    if isinstance(accepted_val, (Validator, MethodType)):
                        if isinstance(accepted_val, Validator):
                            is_valid = accepted_val(returns_val)
                        elif (isinstance(accepted_val, MethodType) and
                                hasattr(accepted_val, '__func__') and
                                isinstance(accepted_val.__func__, Validator)):
                            is_valid = accepted_val(returns_val)
                    elif isinstance(accepted_val, type):
                        is_valid = isinstance(
                            returns_val, accepted_val
                        )
                    else:
                        is_valid = returns_val == accepted_val
                    if is_valid:
                        break
                if not is_valid:
                    raise InvalidReturnTypeError(
                        func, returns_val, self.accepted_returns_values
                    )
            return returns_val
        return decorator_wrapper
