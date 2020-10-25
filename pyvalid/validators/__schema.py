from pyvalid import accepts
from pyvalid.validators import AbstractValidator, Validator


class SchemaValidator(AbstractValidator):
    """Class the validate the input data agains the given schema.

        Example:

        .. code-block:: python
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

    DEFAULT_TYPES = (float, int, complex, dict, bool, set, str, list, tuple)

    @classmethod
    def required_keys(cls, val, schema):
        """Verifies the presence of all required keys."""
        return schema.keys() == val.keys()

    @classmethod
    def schema_compliance(cls, val, schema):
        """Verifies if the input value if the fully compliant with the schema."""
        for key, value in val.items():
            rule = schema.get(key)
            if isinstance(rule, Validator) and not rule(value):
                return False
            elif rule in cls.DEFAULT_TYPES and not isinstance(value, rule):
                return False
        return True

    @accepts(object, dict)
    def __init__(self, schema):
        self.schema = schema
        self.__checkers = {
            SchemaValidator.required_keys: [schema],
            SchemaValidator.schema_compliance: [schema]
        }
        AbstractValidator.__init__(self)

    @accepts(object, dict)
    def __call__(self, val):
        valid = self._check(val)
        return valid

    @property
    def checkers(self):
        return self.__checkers
