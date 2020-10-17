"""This module is designed to control the state of the pyvalid's validation system.
With help of the ``pyvalid.switch`` module it's possible to turn off the pyvalid's
validation so it won't raise an exception anymore even in case of invalid data. And,
of course, it's always possible to turn on the validation system back, when needed.

Example:

.. code-block:: python

    from pyvalid import switch, accepts


    @accepts(str)
    def say_hello(name):
        print('Hello,', name)


    print('Is pyvalid enabled:', switch.is_enabled())
    # Outputs: "Is pyvalid enabled: True"

    say_hello(3)
    # Raises the ArgumentValidationError exception, since the pyvalid's validation
    # is enabled and the "name" argument didn't pass the validation

    switch.turn_off()
    # Now the pyvalid's validation is disabled

    print('Is pyvalid enabled:', switch.is_enabled())
    # Outputs: "Is pyvalid enabled: False"

    say_hello(3)
    # Outputs: "Hello, 3"

    switch.turn_on()
    # And now the pyvalid's validation is enabled back

"""


def turn_on():
    """Enables the pyvalid's validation system.
    """
    globals()['pyvalid_enabled'] = True


def turn_off():
    """Disables the pyvalid's validation system.
    """
    globals()['pyvalid_enabled'] = False


def is_enabled():
    """Returns ``True`` if the pyvalid's validation system is enabled otherwise returns
    ``False`` value.
    """
    if 'pyvalid_enabled' in globals():
        enabled = globals()['pyvalid_enabled']
    else:
        enabled = True
    return enabled
