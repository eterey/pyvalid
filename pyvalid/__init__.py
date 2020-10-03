"""The pyvalid is the Python validation tool for checking a function's input
parameters and return values.

Purposes of the pyvalid package:

#. Provide an ability to validate user input (such as usernames, phone numbers,
   emails, dates and times, etc) and minimize the amount of code required for
   the implementation of the comprehensive validation systems;
#. Add an additional layer of dynamic code analysis for the development and
   testing stages — pyvalid will raise the exception if a function accepts or
   returns unexpected values and you always can disable pyvalid in production
   or whenever you want;
#. Help to catch runtime issues much easier.

The module consists of two decorators: `accepts` and `returns`.
"""

from pyvalid.__accepts import Accepts as accepts
from pyvalid.__returns import Returns as returns
import pyvalid.validators as validators
from pyvalid.__exceptions import ArgumentValidationError, \
    InvalidArgumentNumberError, InvalidReturnTypeError

version = '0.9.6'

__all__ = [
    'accepts',
    'returns',
    'validators',
    'switch',
    'version',
    'ArgumentValidationError',
    'InvalidArgumentNumberError',
    'InvalidReturnTypeError'
]
