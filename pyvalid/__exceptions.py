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
