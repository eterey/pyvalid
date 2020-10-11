"""
The pyvalid is the Python validation tool for checking a function's input parameters
and return values.
 Purposes of the pyvalid package:
 #. Provide an ability to validate a user input (such as usernames, phone numbers,
   emails, dates and times, etc) and minimize the amount of code required for the
   implementation of the comprehensive validation systems;
#. Add an additional layer of dynamic code analysis for the development and testing
   stages — pyvalid will raise the exception if a function accepts or returns unexpected
   values and it's always possible to disable pyvalid in production if needed.
#. Help to catch runtime issues.
"""

from pyvalid.__accepts import Accepts as accepts
from pyvalid.__returns import Returns as returns
from pyvalid import switch
from pyvalid import validators
from pyvalid.__exceptions import PyvalidError, ArgumentValidationError, \
    InvalidArgumentNumberError, InvalidReturnTypeError


version = '1.0.4'


__all__ = [
    'accepts',
    'returns',
    'switch',
    'validators',
    'version',
    'PyvalidError',
    'ArgumentValidationError',
    'InvalidArgumentNumberError',
    'InvalidReturnTypeError'
]
