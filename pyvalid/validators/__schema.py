try:
    from collections.abc import Iterable, Container
except ImportError:
    from collections import Iterable, Container

from pyvalid import accepts
from pyvalid.validators import AbstractValidator, Validator


class SchemaValidator(AbstractValidator):
    """
        Class the validate the input data agains the given schema.
        example:
        user_schema = SchemaValidator({
        'name': StringValidator(re_pattern=r'^[A-Za-z]+\s?[A-Za-z]+\s?[A-Za-z]+$'),
        'birthyear': NumberValidator(min_val=1990, max_val=2010),
        'rating': float,
        # 'bio': [StringValidator(max_len=2048), None]
        })

        new_schema = SchemaValidator({
            'name': StringValidator(re_pattern=r'^[A-Za-z]+\s?[A-Za-z]+\s?[A-Za-z]+$'),
            'birthyear': NumberValidator(min_val=1890, max_val=2020),
            'rating': float,
            'bio': StringValidator(min_len=1),
            'new_data': user_schema
        })


        # So we can use schemas for `@accepts` and `@returns`
        # @accepts(new_user=user_schema)
        # def register_user(new_user):
        #     # some logic here
        #     pass


        # Or we can call them directly to validate some data
        # user_schema({
        #     'name': 'Max',
        #     'birthyear': -42,  # will cause a validator error
        #     'bio': None,
        #     'rating': 8.0
        #     # the `address` attribute is missing, what will cause another error even if we fix `birthyear`
        # })

        old_user = {
            'name': 'Nagesh',
            'birthyear': 1994,  # will cause a validator error
            # 'bio': None,
            'rating': 8.0
        }

        @accepts(new_user=new_schema, X=StringValidator(re_pattern=r'^[A-Za-z]+\s?[A-Za-z]+\s?[A-Za-z]+$'))
        def register_users(new_user, X):
            # some logic here
            pass

        new_user = {
            'name': 'Nandeesh',
            'birthyear': 2020,  # will cause a validator error
            'bio': "Nagesh",
            'rating': 8.0,
            'new_data': old_user
            # the `address` attribute is missing, what will cause another error even if we fix `birthyear`
        }

        register_users(new_user, "Nandan")

    """

    SCHEMA_TYPES = (dict,)
    DEFAULT_TYPES = (float, int, complex, dict, bool, set, str, list, tuple)

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
        for key, value in self.schema.items():
            if self.__key_checker(self.schema.get(key)):
                validator = self.schema.get(key)
                self.__checkers.update(validator.checkers)
                # print(validator.checkers)
            elif self.schema.get(key) in self.DEFAULT_TYPES:
                pass
        self.__key_checker(schema)
        AbstractValidator.__init__(self)

    def __call__(self, val):
        is_schema = isinstance(val, SchemaValidator.SCHEMA_TYPES)

        # check if the input has all the keys
        valid_keys = self.__validate_keys(val)
        valid_args = False
        if valid_keys:
            validators = {}
            for key, value in val.items():
                if isinstance(self.schema.get(key), Validator):
                    validators.update({key: value})
                elif self.schema.get(key) in self.DEFAULT_TYPES:
                    if not type(value)==self.schema.get(key):
                        return False
            valid_args = self._check(validators)
        else:
            raise Exception("Schema Keys Accepted are {} but got {}".format(list(self.schema.keys()), list(val.keys())))
        valid = is_schema and valid_args

        # TODO Handle the Exception properly instead of ArgumentValidationError
        return valid

    def _check(self, val):
        valid = False
        for key, value in val.items():
            valid = True
            if isinstance(self.schema.get(key), SchemaValidator):
                valid = self.schema.get(key).__call__(value)
            else:
                for checker_func, checker_args in self.schema.get(key).checkers.items():
                    valid = checker_func(value, *checker_args)
                    if not valid:
                        return False
        return valid

    @property
    def checkers(self):
        return self.__checkers
