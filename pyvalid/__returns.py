from collections import Callable
from pyvalid.__exceptions import InvalidReturnType


class Returns(Callable):
    """A decorator to validate the returns value of a given function.
    """

    def __init__(self, *accepted_returns_values):
        self.accepted_returns_values = accepted_returns_values

    def __call__(self, func):
        def decorator_wrapper(*func_args, **func_kwargs):
            from pyvalid.validators import Validator
            returns_val = func(*func_args, **func_kwargs)
            if self.accepted_returns_values:
                is_valid = False
                for accepted_returns_val in self.accepted_returns_values:
                    if isinstance(accepted_returns_val, Validator):
                        is_valid = accepted_returns_val(returns_val)
                    elif isinstance(accepted_returns_val, type):
                        is_valid = isinstance(
                            returns_val, accepted_returns_val
                        )
                    else:
                        is_valid = returns_val == accepted_returns_val
                    if is_valid:
                        break
                if not is_valid:
                    raise InvalidReturnType(type(returns_val), func.__name__)
            return returns_val
        return decorator_wrapper
