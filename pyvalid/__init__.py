from pyvalid.__accepts import Accepts
from pyvalid.__returns import Returns
from pyvalid.__exceptions import InvalidArgumentNumberError, \
    InvalidReturnType, ArgumentValidationError


accepts = Accepts
returns = Returns
version = '0.9.5'


__all__ = [
    'validators',
    'switch',
    'version',
    'accepts',
    'returns',
    'InvalidArgumentNumberError',
    'InvalidReturnType',
    'ArgumentValidationError'
]
