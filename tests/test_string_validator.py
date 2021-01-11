import re
import unittest

from pyvalid.validators import StringValidator


class StringValidatorTestCase(unittest.TestCase):

    def test_min_len(self):
        validator = StringValidator(min_len=2)
        self.assertTrue(validator('Python').status)
        self.assertTrue(validator('Py').status)
        self.assertFalse(validator('P').status)
        self.assertFalse(validator(None).status)

    def test_max_len(self):
        validator = StringValidator(max_len=6)
        self.assertTrue(validator(str()).status)
        self.assertTrue(validator('Python').status)
        self.assertFalse(validator('Python3').status)
        self.assertFalse(validator(None).status)

    def test_in_range(self):
        validator = StringValidator(
            in_range=['CPython', 'PyPy', 'IronPython', 'Jython', 'Cython']
        )
        self.assertTrue(validator('PyPy').status)
        self.assertTrue(validator('Cython').status)
        self.assertFalse(validator('Ruby').status)
        self.assertFalse(validator(None).status)

    def test_not_in_range(self):
        validator = StringValidator(
            not_in_range=['CPython', 'PyPy', 'IronPython', 'Jython', 'Cython']
        )
        self.assertTrue(validator('Ruby').status)
        self.assertTrue(validator('Java').status)
        self.assertFalse(validator('CPython').status)
        self.assertFalse(validator(None).status)

    def test_re(self):
        # Allowed characters are: latin alphabet letters and digits
        validator = StringValidator(re_pattern='^[a-zA-Z0-9]+$')
        self.assertTrue(validator('pyvalid').status)
        self.assertTrue(validator('42').status)
        self.assertFalse(validator('__pyvalid__').status)
        # Regular expression is broken
        validator = StringValidator(re_pattern=':)')
        self.assertFalse(validator('pyvalid').status)
        self.assertFalse(validator(':)').status)
        # Try to use regular expression with flag
        validator = StringValidator(
            re_pattern='^pyvalid$', re_flags=re.IGNORECASE
        )
        self.assertTrue(validator('pyvalid').status)
        self.assertTrue(validator('PyValid').status)
        self.assertFalse(validator('42').status)
        self.assertFalse(validator(None).status)

    def test_mixed(self):
        validator = StringValidator(
            min_len=6, max_len=64,
            not_in_range=['password', 'qwerty', '123456789', 'sunshine'],
        )
        self.assertTrue(validator('Super_Mega_Strong_Password_2000').status)
        self.assertTrue(validator('_' * 6).status)
        self.assertFalse(validator('_' * 3).status)
        self.assertFalse(validator('_' * 128).status)
        self.assertFalse(validator('sunshine').status)
        self.assertFalse(validator(None).status)


if __name__ == '__main__':
    unittest.main()
