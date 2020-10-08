import unittest

import pyvalid


class TestSwitch(unittest.TestCase):

    def setUp(self):
        @pyvalid.returns(True)
        @pyvalid.accepts(True)
        def func1(val):
            return val
        self.func1 = func1

    def test_default_state(self):
        # Validators must be enabled by default.
        self.assertTrue(pyvalid.switch.is_enabled())

    def test_turn_off(self):
        pyvalid.switch.turn_off()
        val = self.func1(False)
        self.assertFalse(val)

    def test_turn_on(self):
        pyvalid.switch.turn_on()
        val = self.func1(True)
        self.assertTrue(val)
        self.assertRaises(
            pyvalid.ArgumentValidationError, self.func1, False
        )


if __name__ == '__main__':
    unittest.main()
