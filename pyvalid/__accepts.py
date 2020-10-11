from functools import wraps
from types import MethodType
from sys import version_info
if version_info < (3, 0, 0):
    from inspect import getargspec
else:
    from inspect import getfullargspec as getargspec
try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable

from pyvalid.__exceptions import InvalidArgumentNumberError, ArgumentValidationError
from pyvalid.switch import is_enabled


class Accepts(Callable):
    """
    ``pyvalid.accepts(*allowed_arg_values, **allowed_kwargs_values)``
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    The decorator which validates input parameters of the wrapped function.

    To use it, we need to specify the list of allowed types or values. If the function’s
    input doesn’t match the allowed types/values, one of the following errors will be
    thrown:

    * ``pyvalid.ArgumentValidationError`` — when the actual type/value of the function’s
      argument is different from the expected one;
    * ``pyvalid.InvalidArgumentNumberError`` — when the number/position of function’s
      arguments is incorrect.

    Examples of usage:

    Let's define the ``multiply`` function, which accepts only ``int`` values, and see
    how does it work with other types.

    .. code-block:: python

        from pyvalid import accepts


        @accepts(int, int)
        def multiply(num_1, num_2):
            return num_1 * num_2


        multiply(4, 2)
        # Returns 8.

        multiply(3.14, 8)
        # Raises the ArgumentValidationError exception, since the 1st argument is the
        # float value, when we're expecting int values only.

        multiply(3, 'pyvalid')
        # Raises the ArgumentValidationError exception, since the 2nd argument is the
        # str value, when we're expecting int values only.

        multiply(128)
        # Raises the InvalidArgumentNumberError exception, since the second argument
        # is missing.
    """

    def __init__(self, *allowed_arg_values, **allowed_kwargs_values):
        self.allowed_arg_values = allowed_arg_values
        self.allowed_kwargs_values = allowed_kwargs_values
        self.allowed_params = list()
        self.optional_args = list()

    def __call__(self, func):
        @wraps(func)
        def decorator_wrapper(*func_args, **func_kwargs):
            perform_validation = all((
                is_enabled(),
                self.allowed_arg_values or self.allowed_kwargs_values
            ))
            if perform_validation:
                # Forget all information about function arguments.
                self.allowed_params[:] = list()
                self.optional_args[:] = list()
                # Collect information about fresh arguments.
                args_info = getargspec(func)
                self.__scan_func(args_info)
                self.__pep_0468_fix(func)
                # Validate function arguments.
                self.__validate_args(func, func_args, func_kwargs)
            # Call function.
            return func(*func_args, **func_kwargs)
        return decorator_wrapper

    def __wrap_allowed_val(self, value):
        """Wrap allowed value in the list if not wrapped yet.
        """
        if isinstance(value, tuple):
            value = list(value)
        elif not isinstance(value, list):
            value = [value]
        return value

    def __scan_func(self, args_info):
        """Collects information about allowed values in the following format:

        .. code-block:: python

            (
                (<argument name>, <allowed types and values>),
                (<argument name>, <allowed types and values>),
                ...
            )

        Args:
            args_info (inspect.FullArgSpec):
                Information about function arguments.
        """
        # Process args.
        for i, allowed_val in enumerate(self.allowed_arg_values):
            allowed_val = self.__wrap_allowed_val(allowed_val)
            # Add default value (if exists) in list of allowed values.
            if args_info.defaults:
                def_range = len(args_info.defaults) - len(args_info.args[i:])
                if def_range >= 0:
                    self.optional_args.append(i)
                    default_value = args_info.defaults[def_range]
                    allowed_val.append(default_value)
            # Try to detect current argument name.
            if len(args_info.args) > i:
                arg_name = args_info.args[i]
            else:
                arg_name = None
                self.optional_args.append(i)
            # Save info about current argument and his allowed values.
            self.allowed_params.append((arg_name, allowed_val))
        # Process kwargs.
        for arg_name, allowed_val in self.allowed_kwargs_values.items():
            allowed_val = self.__wrap_allowed_val(allowed_val)
            # Mark current argument as optional.
            i = len(self.allowed_params)
            self.optional_args.append(i)
            # Save info about current argument and his allowed values.
            self.allowed_params.append((arg_name, allowed_val))

    def __validate_args(self, func, args, kwargs):
        """Compare value of each required argument with list of allowed values.

        Args:
            func (types.FunctionType):
                Function to validate.
            args (list):
                Collection of the position arguments.
            kwargs (dict):
                Collection of the keyword arguments.

        Raises:
            InvalidArgumentNumberError:
                When position or count of the arguments is incorrect.
            ArgumentValidationError:
                When encountered unexpected argument value.
        """
        from pyvalid.validators import Validator
        for i, (arg_name, allowed_values) in enumerate(self.allowed_params):
            if i < len(args):
                value = args[i]
            else:
                if arg_name in kwargs:
                    value = kwargs[arg_name]
                elif i in self.optional_args:
                    continue
                else:
                    raise InvalidArgumentNumberError(func)
            is_valid = False
            for allowed_val in allowed_values:
                is_validator = (
                    isinstance(allowed_val, Validator) or
                    (
                        isinstance(allowed_val, MethodType) and
                        hasattr(allowed_val, '__func__') and
                        isinstance(allowed_val.__func__, Validator)
                    )
                )
                if is_validator:
                    is_valid = allowed_val(value)
                elif isinstance(allowed_val, type):
                    is_valid = isinstance(value, allowed_val)
                else:
                    is_valid = value == allowed_val
                if is_valid:
                    break
            if not is_valid:
                ord_num = self.__ordinal(i + 1)
                raise ArgumentValidationError(func, ord_num, value, allowed_values)

    def __ordinal(self, num):
        """Returns the ordinal number of a given integer, as a string.
        eg. 1 -> 1st, 2 -> 2nd, 3 -> 3rd, etc.
        """
        if 10 <= num % 100 < 20:
            return str(num) + 'th'
        else:
            ord_info = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
            return '{}{}'.format(num, ord_info)

    def __pep_0468_fix(self, func):
        """Fixes the issue with preserving the order of function's arguments. So far,
        the issue exists in the Python 3.5 only. More details can be found on the
        "PEP 468" page: https://www.python.org/dev/peps/pep-0468/
        """
        is_broken_py = (version_info.major, version_info.minor) == (3, 5)
        if not is_broken_py:
            return False
        from inspect import signature, Parameter
        func_signature = signature(func)
        func_parameters = func_signature.parameters.values()
        parameters_order = dict()
        for param_index, param in enumerate(func_parameters):
            if param.kind is Parameter.VAR_KEYWORD:
                continue
            parameters_order[param.name] = param_index
        last_param_pos = len(self.allowed_params)
        self.allowed_params.sort(
            key=lambda param: parameters_order.get(param[0], last_param_pos)
        )
