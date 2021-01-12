import unittest

from pyvalid.validators import NumberValidator
from pyvalid.validators import IsValid


class NumberValidatorTestCase(unittest.TestCase):

    def test_number_type(self):
        validator = NumberValidator(number_type=int)
        self.assertTrue(validator(12).status)
        self.assertFalse(validator(10.56).status)

        validator = NumberValidator(number_type=float)
        self.assertTrue(validator(10.56).status)
        self.assertFalse(validator(12).status)

    def test_min_val(self):
        validator = NumberValidator(min_val=-3.14)
        self.assertTrue(validator(3.14).status)
        self.assertTrue(validator(-3.14).status)
        self.assertFalse(validator(-273.15).status)
        self.assertFalse(validator(None).status)

    def test_max_val(self):
        validator = NumberValidator(max_val=42)
        self.assertTrue(validator(8).status)
        self.assertTrue(validator(0).status)
        self.assertFalse(validator(512).status)
        self.assertFalse(validator(None).status)

    def test_in_range(self):
        validator = NumberValidator(
            in_range=[2**x for x in range(16)]
        )
        self.assertTrue(validator(1).status)
        self.assertTrue(validator(256.0).status)
        self.assertFalse(validator(0).status)
        self.assertFalse(validator(None).status)

    def test_not_in_range(self):
        validator = NumberValidator(
            not_in_range=[2**x for x in range(16)]
        )
        self.assertTrue(validator(0).status)
        self.assertTrue(validator(-1).status)
        self.assertFalse(validator(2).status)
        self.assertFalse(validator(None).status)

    def test_mixed(self):
        with self.assertRaises(ValueError):
            NumberValidator(min_val=100, max_val=50)

        validator = NumberValidator(
            min_val=0, max_val=2**16,
            not_in_range=[2**x for x in range(16)]
        )
        self.assertTrue(validator(0).status)
        self.assertTrue(validator(2**16 - 0.1).status)
        self.assertFalse(validator(2**16 + 0.1).status)
        self.assertFalse(validator(8).status)
        self.assertFalse(validator(-8).status)
        self.assertFalse(validator(None).status)


if __name__ == '__main__':
    unittest.main()
