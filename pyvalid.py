import inspect
import functools
from collections import Callable


class InvalidArgumentNumberError(ValueError):
    """Raised when the number or position of arguments supplied to a function
    is incorrect.
    """
    def __init__(self, func_name):
        self.error = 'Invalid number or position of arguments for {}()'.format(
            func_name
        )

    def __str__(self):
        return self.error


class ArgumentValidationError(ValueError):
    """Raised when the type of an argument to a function is not what it
    should be.
    """
    def __init__(self, arg_num, func_name, accepted_arg_values):
        self.error = 'The {} argument of {}() is not in a {}'.format(
            arg_num, func_name, accepted_arg_values
        )

    def __str__(self):
        return self.error


class InvalidReturnType(ValueError):
    """Raised when the return value is the wrong type.
    """
    def __init__(self, return_type, func_name):
        self.error = 'Invalid return type {} for {}()'.format(
            return_type, func_name
        )

    def __str__(self):
        return self.error


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


class accepts(Callable):
    """A decorator to validate a types of input parameters 
    for a given function.
    """

    def __init__(self, *accepted_arg_values):
        self.accepted_arg_values = accepted_arg_values
        self.accepted_args = list()
        self.optional_args = list()

    def __call__(self, func):
        @functools.wraps(func)
        def decorator_wrapper(*func_args, **func_kwargs):
            args_info = inspect.getfullargspec(func)
            args = args_info.args
            if args_info.defaults is None:
                defaults = tuple()
            else:
                defaults = args_info.defaults
            if args and self.accepted_arg_values:
                # Forget all information about function arguments.
                self.accepted_args.clear()
                self.optional_args.clear()
                # Collect information about fresh arguments.
                self.__scan_func(args, defaults)
                # Validate function arguments.
                self.__validate_args(func.__name__, func_args, func_kwargs)
            # Call function.
            return func(*func_args, **func_kwargs)
        return decorator_wrapper

    def __scan_func(self, args, defaults):
        """Collect information about accepted arguments in following format:
            (
                (<argument name>, <accepted types and values>),
                (<argument name>, <accepted types and values>),
                ...
            )

        Args:
            func (collections.Callable): Function for scan.
            args_info (inspect.FullArgSpec): Information about function
                arguments.
        """
        for i, accepted_arg_type in enumerate(self.accepted_arg_values):
            if isinstance(accepted_arg_type, tuple):
                accepted_arg_type = list(accepted_arg_type)
            else:
                accepted_arg_type = [accepted_arg_type]
            def_range = len(defaults) - len(args[i:])
            if def_range >= 0:
                self.optional_args.append(i)
                accepted_arg_type.append(defaults[def_range])
            self.accepted_args.append((args[i], accepted_arg_type))

    def __validate_args(self, func_name, args, kwargs):
        """Compare value of each required argument with list of
        accepted values.

        Args:
            func_name (str): Function name.
            args (list): Collection of the position arguments.
            kwargs (dict): Collection of the keyword arguments.

        Raises:
            InvalidArgumentNumberError: When position or count of the arguments
                is incorrect.
            ArgumentValidationError: When encountered unexpected argument
                value.
        """
        for i, (arg_name, accepted_values) in enumerate(self.accepted_args):
            if i < len(args):
                value = args[i]
            else:
                if arg_name in kwargs:
                    value = kwargs[arg_name]
                elif i in self.optional_args:
                    continue
                else:
                    raise InvalidArgumentNumberError(func_name)
            is_valid = False
            for accepted_val in accepted_values:
                if isinstance(accepted_val, type):
                    is_valid = isinstance(value, accepted_val)
                else:
                    is_valid = value == accepted_val
                if is_valid:
                    break
            if not is_valid:
                ord_num = self.__ordinal(i + 1)
                raise ArgumentValidationError(
                    ord_num,
                    func_name,
                    accepted_values
                )

    def __ordinal(self, num):
        """Returns the ordinal number of a given integer, as a string.
        eg. 1 -> 1st, 2 -> 2nd, 3 -> 3rd, etc.
        """
        if 10 <= num % 100 < 20:
            return str(num) + 'th'
        else:
            ord_info = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
            return '{}{}'.format(num, ord_info)
