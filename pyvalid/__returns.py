from collections import Callable
from pyvalid.__exceptions import InvalidReturnType


class returns(Callable):
    """A decorator to validate the returns value of a given function.
    """

    def __init__(self, *accepted_returns_values):
        self.accepted_returns_values = accepted_returns_values

    def __call__(self, func):
        def decorator_wrapper(*func_args, **func_kwargs):
            returns_value = func(*func_args, **func_kwargs)
            if self.accepted_returns_values:
                is_valid = False
                for accepted_returns_value in self.accepted_returns_values:
                    if isinstance(accepted_returns_value, type):
                        is_valid = isinstance(
                            returns_value, accepted_returns_value
                        )
                    else:
                        is_valid = returns_value == accepted_returns_value
                    if is_valid:
                        break
                if not is_valid:
                    raise InvalidReturnType(type(returns_value), func.__name__)
            return returns_value
        return decorator_wrapper