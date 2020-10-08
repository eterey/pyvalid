class PyvalidError(ValueError):
    def __get_func_name__(self, func):
        func_name = func.__name__
        from sys import version_info
        py_ver = (version_info.major, version_info.minor)
        has_signature_support = py_ver >= (3, 3)
        if has_signature_support:
            from inspect import signature
            func_name += str(signature(func))
        else:
            func_name += '()'
        return func_name


class InvalidArgumentNumberError(PyvalidError):
    """Raised when the number or position of arguments supplied to a function is
    incorrect.
    """
    def __init__(self, func):
        error_message_template = (
            'Invalid number or position of arguments for the "{}" function.'
        )
        self.error = error_message_template.format(
            self.__get_func_name__(func)
        )

    def __str__(self):
        return self.error


class ArgumentValidationError(PyvalidError):
    """Raised when the type of an argument to a function is not what it should be.
    """
    def __init__(self, func, arg_num, actual_value, allowed_arg_values):
        error_message_template = (
            'The {} argument of the "{}" function is "{}" of the "{}" type, while '
            'expected values are: "{}".'
        )
        self.error = error_message_template.format(
            arg_num,
            self.__get_func_name__(func),
            actual_value,
            type(actual_value),
            allowed_arg_values
        )

    def __str__(self):
        return self.error


class InvalidReturnTypeError(PyvalidError):
    """Raised when the return value is the wrong type.
    """
    def __init__(self, func, actual_value, allowed_return_values):
        error_message_template = (
            'Invalid return value "{}" of the "{}" type for the "{}" function, while '
            'expected values are: "{}".'
        )
        self.error = error_message_template.format(
            actual_value,
            type(actual_value),
            self.__get_func_name__(func),
            allowed_return_values
        )

    def __str__(self):
        return self.error
