pyvalid
-------

.. image:: https://img.shields.io/codecov/c/github/uzumaxy/pyvalid.svg?style=plastic
.. image:: https://img.shields.io/github/workflow/status/uzumaxy/pyvalid/Python%20package?style=plastic

The pyvalid is the Python validation tool for checking a function's input
parameters and return values.

Purposes of the pyvalid package:

#. Provide an ability to validate user input (such as usernames, phone numbers,
   emails, dates and times, etc) and minimize the amount of code required for
   the implementation of the comprehensive validation systems;
#. Add an additional layer of dynamic code analysis for the development and
   testing stages — pyvalid will raise the exception if a function accepts or
   returns unexpected values and you always can disable pyvalid in production
   or whenever you want;
#. Help to catch runtime issues much easier.

The module consists of two decorators: `accepts` and `returns`.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`accepts(*accepted_arg_values, **accepted_kwargs_values)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A decorator for validating types and values of input parameters of a given function.
You can pass the set of accepted types and values or validation function as decorator's input parameters.
Validation process can raise the following exceptions:

* `pyvalid.InvalidArgumentNumberError` — when the number or position of arguments supplied to a function is incorrect.
* `pyvalid.ArgumentValidationError` — when the type of an argument to a function is not what it should be.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`returns(*accepted_returns_values)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A decorator for validating the return value of a given function.
You can pass the set of accepted types and values or validation function as a decorator's input parameters.
Validation process can raise `pyvalid.InvalidReturnTypeError` when the return value is not in the collection of supported values and types.


How to install
++++++++++++++

* With PyPI: `pip install -U pyvalid`
* Manually: `python setup.py install`


Example of usage
++++++++++++++++

Function `calc` in example below has next limitations:

* Can return only int or float value;
* First parameter must be only of type str;
* Second parameter must be of type int or equals to 2.0;
* Third parameter must be of type int or float.


.. code-block:: python

    from pyvalid import accepts, returns


    @returns(int, float)
    @accepts(str, (int, 2.0), (int, float))
    def calc(operator, val1, val2, val3):
        expression = '{v1} {op} {v2} {op} {v3}'.format(
            op=operator,
            v1=val1, v2=val2, v3=val3
        )
        return eval(expression)


    # Output: 24.
    print(calc('*', 2, 3, 4))

    # Output: 24.0.
    print(calc(operator='*', val1=2, val2=3.0, val3=4))

    # Output: 24.0.
    print(calc('*', 2.0, 3, 4))

    # Raises pyvalid.ArgumentValidationError exception,
    # because second argument has unsupported value.
    print(calc('*', 3.14, 3, 4))


    # Raises pyvalid.InvalidReturnTypeError exception,
    # because returns value is of type str.
    print(calc('*', 2, 3, '"4"'))


Here is an example of usage `pyvalid` module in context of classes.
Pay attention to the method `connect` of the class `SqlDriver`.
This method is a good demonstration of usage `accepts` decorator for functions with keyword arguments.

.. code-block:: python

    from pyvalid import accepts, returns
    from collections import Iterable


    class SqlDriver(object):

        @returns(bool)
        @accepts(object, host=str, port=int, usr=str, pwd=str, db=[str, None])
        def connect(self, **kwargs):
            connection_string = \
                'tsql -S {host} -p {port} -U {usr} -P {pwd} -D {db}'.format(**kwargs)
            try:
                print('Establishing connection: "{}"'.format(connection_string))
                # Create connection..
                success = True
            except:
                success = False
            return success

        @returns(bool)
        def close(self):
            try:
                print('Closing connection')
                # Close connection..
                success = True
            except:
                success = False
            return success

        @returns(None, dict)
        @accepts(object, str, Iterable)
        def query(self, sql, params=None):
            try:
                query_info = 'Processing request "{}"'.format(sql)
                if params is not None:
                    query_info += ' with following params: ' + ', '.join(params)
                print(query_info)
                # Process request..
                data = dict()
            except:
                data = None
            return data


    sql_driver = SqlDriver()

    conn_params = {
        'host': '8.8.8.8',
        'port': 1433,
        'usr': 'admin',
        'pwd': 'Super_Mega_Strong_Password_2000',
        'db': 'info_tech'
    }
    sql_driver.connect(**conn_params)

    sql = r'SELECT * FROM ProgrammingLang'
    pl = sql_driver.query(sql)

    sql = r'SELECT * FROM ProgrammingLang WHERE name=?'
    python_pl = sql_driver.query(sql, ('Python',))

    sql_driver.close()


Following example with class `User` will show you how to use `pyvalid` module to validate some value with using validation function.

.. code-block:: python

    from pyvalid import accepts
    from pyvalid.validators import is_validator


    class User(object):

        class Validator(object):

            unsafe_passwords = [
                '111111', '000000', '123123',
                '123456', '12345678', '1234567890',
                'qwerty', 'sunshine', 'password',
            ]

            @classmethod
            @is_validator
            def login_checker(cls, login):
                is_valid = isinstance(login, str) and 1 <= len(login) <= 16
                if is_valid:
                    for reg_user in User.registered:
                        if login == reg_user.login:
                            is_valid = False
                            break
                return is_valid

            @classmethod
            @is_validator
            def password_checker(cls, password):
                is_valid = isinstance(password, str) and \
                    (6 <= len(password) <= 32) and \
                    (password not in cls.unsafe_passwords)
                return is_valid

        registered = list()

        def __init__(self, login, password):
            self.__login = None
            self.login = login
            self.__password = None
            self.password = password
            User.registered.append(self)

        @property
        def login(self):
            return self.__login

        @login.setter
        @accepts(object, Validator.login_checker)
        def login(self, value):
            self.__login = value

        @property
        def password(self):
            return self.__password

        @password.setter
        @accepts(object, Validator.password_checker)
        def password(self, value):
            self.__password = value


    user = User('admin', 'Super_Mega_Strong_Password_2000')

    # Output: admin Super_Mega_Strong_Password_2000
    print(user.login, user.password)

    # Raise pyvalid.ArgumentValidationError exception,
    # because User.Validator.password_checker method
    # returns False value.
    user.password = 'qwerty'

    # Raise pyvalid.ArgumentValidationError exception,
    # because User.Validator.login_checker method
    # returns False value.
    user = User('admin', 'Super_Mega_Strong_Password_2001')


License
+++++++

Note that this project is distributed under the `MIT License <LICENSE>`_.
