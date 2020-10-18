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

    def test_min_len(self):
        validator = SchemaValidator({
            'name': StringValidator(re_pattern=r'^[A-Za-z]+\s?[A-Za-z]+\s?[A-Za-z]+$'),
            'birthyear': NumberValidator(min_val=1890, max_val=2020),
            'rating': float,
            'bio': [StringValidator(max_len=1024), None]
        })
        self.assertTrue(validator(self.new_user))
        self.new_user['rating'] = 8
        self.assertFalse(validator(self.new_user))
        self.new_user.__delitem__('rating')
        self.assertRaises(Exception, validator,self.new_user)


if __name__ == '__main__':
    unittest.main()
