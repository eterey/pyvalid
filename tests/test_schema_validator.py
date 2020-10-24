import unittest

from pyvalid.validators import SchemaValidator, StringValidator, NumberValidator


class SchemaValidatorTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.new_user = {
            'rating': 8.0,
            'name': 'Max',
            'birthyear': 1994,  # will cause a validator error
            'bio': None
            # the `address` attribute is missing, what will cause another error even if we fix `birthyear`
        }

    def test_schema(self):
        schema = SchemaValidator({
            'name': StringValidator(re_pattern=r'^[A-Za-z]+\s?[A-Za-z]+\s?[A-Za-z]+$'),
            'birthyear': NumberValidator(min_val=1890, max_val=2020),
            'rating': float,
            'bio': [StringValidator(max_len=1024), None]
        })
        self.assertTrue(schema(self.new_user))
        self.new_user['rating'] = 8
        self.assertFalse(schema(self.new_user))
        self.new_user.__delitem__('rating')
        self.assertRaises(Exception, schema, self.new_user)

    def test_schema_input(self):
        schema = SchemaValidator({
            'name': StringValidator(re_pattern=r'^[A-Za-z]+\s?[A-Za-z]+\s?[A-Za-z]+$'),
            'birthyear': NumberValidator(min_val=1890, max_val=2020),
            'rating': float,
            'bio': [StringValidator(max_len=1024), None]
        })
        sub_schema = SchemaValidator({
            'name': StringValidator(re_pattern=r'^[A-Za-z]+\s?[A-Za-z]+\s?[A-Za-z]+$'),
            'birthyear': NumberValidator(min_val=1890, max_val=2020),
            'manager': schema
        })

        default_user = {
            'name': 'Max',
            'birthyear': 1994,  # will cause a validator error
            'manager': self.new_user
        }
        self.assertTrue(sub_schema(default_user))
        self.new_user['rating'] = 8
        self.assertFalse(sub_schema(default_user))
        self.new_user.__delitem__('rating')
        self.assertRaises(Exception, sub_schema, default_user)


if __name__ == '__main__':
    unittest.main()
