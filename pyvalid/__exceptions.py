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
    def __init__(self, arg_num, func_name, actual_value, accepted_arg_values):
        error_message_template = (
            'The {} argument of the "{}()" function is "{}" of the "{}" '
            'type, while expected values are: "{}".'
        )
        self.error = error_message_template.format(
            arg_num,
            func_name,
            actual_value,
            type(actual_value),
            accepted_arg_values
        )

    def __str__(self):
        return self.error


class InvalidReturnTypeError(ValueError):
    """Raised when the return value is the wrong type.
    """
    def __init__(self, return_type, func_name):
        error_message_template = \
            'Invalid return type "{}" for the "{}()" function.'
        self.error = error_message_template.format(return_type, func_name)

    def __str__(self):
        return self.error
