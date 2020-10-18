try:
    from collections.abc import Iterable, Container
except ImportError:
    from collections import Iterable, Container

from pyvalid import accepts
from pyvalid.validators import AbstractValidator,Validator


class SchemaValidator(AbstractValidator):

    schema_types = (dict,)

    @staticmethod
    def __key_checker(val):
        return isinstance(val, Validator)

    def __validate_keys(self, val):
        return self.schema.keys() == val.keys()

    @accepts(object)
    def __init__(self, schema: dict, **kwargs):
        self.schema = schema
        self.__checkers = {
        }
        self.__key_checker(schema)
        AbstractValidator.__init__(self)

    def __call__(self, val):
        is_schema = isinstance(val, SchemaValidator.schema_types)

        # check if the input has all the keys
        valid_keys = self.__validate_keys(val)
        valid_args = False
        if valid_keys:
            for key, value in val.items():
                if self.__key_checker(self.schema.get(key)):
                    valid_args = self.schema.get(key)._check(value)
                elif self.schema.get(key) in [float, int, complex, dict, bool, set, str, list, tuple]:
                    valid_args = isinstance(val[key],self.schema.get(key))

                # Return False, even if one of the key has invalid data type. So further checks are not done
                if not valid_args:
                    return valid_args
        else:
            raise Exception("Schema Keys Accepted are {} but got {}".format(list(self.schema.keys()), list(val.keys())))
        valid = is_schema and valid_args

        # TODO Handle the Exception properly instead of ArgumentValidationError
        return valid

    @property
    def checkers(self):
        return self.__checkers
