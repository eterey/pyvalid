import unittest

from pyvalid.validators import SchemaValidator, StringValidator, NumberValidator


class SchemaValidatorTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.user = {
            'rating': 8.0,
            'name': 'Max',
            'birthyear': 1994,
            'bio': None
        }

    def test_schema(self):
        schema = SchemaValidator({
            'name': StringValidator(re_pattern=r'^[A-Za-z]+\s?[A-Za-z]+\s?[A-Za-z]+$'),
            'birthyear': NumberValidator(min_val=1890, max_val=2020),
            'rating': float,
            'bio': [StringValidator(max_len=1024), None]
        })
        self.assertTrue(schema(self.user))
        self.user['rating'] = 8
        self.assertFalse(schema(self.user))
        self.user.__delitem__('rating')
        self.assertFalse(schema(self.user))
        self.assertFalse(schema(None))

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
            'manager': self.user
        }
        self.assertTrue(sub_schema(default_user))
        self.user['rating'] = 8
        self.assertFalse(sub_schema(default_user))
        self.user.__delitem__('rating')
        self.assertFalse(sub_schema(default_user))


if __name__ == '__main__':
    unittest.main()
