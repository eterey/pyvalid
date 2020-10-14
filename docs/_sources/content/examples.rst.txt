Examples
--------

Function ``calculate`` in the example below has the following limitations:

* Function should return ``int`` or ``float`` values only;
* First parameter must be ``str`` value;
* Second parameter must be ``int`` value or be equal to the ``2.0``;
* Third parameter must be ``int`` or ``float`` value.

.. code-block:: python

    from pyvalid import accepts, returns


    @returns(int, float)
    @accepts(str, (int, 2.0), (int, float))
    def calculate(operator, val1, val2, val3):
        expression = '{v1} {op} {v2} {op} {v3}'.format(
            op=operator, v1=val1, v2=val2, v3=val3
        )
        return eval(expression)


    calculate('*', 2, 3, 4)
    # Returns 24.

    calculate(operator='*', val1=2, val2=3.0, val3=4)
    # Returns 24.0.

    calculate('*', 2.0, 3, 4)
    # Still returns 24.0.

    calculate('*', 3.14, 3, 4)
    # Raises the ArgumentValidationError exception, because the second
    # argument is not valid.

    calculate('*', 2, 3, '"4"')
    # Raises the InvalidReturnTypeError exception, because of invalid return
    # value: function returns the str value, when only int and float values
    # are allowed.


The example below demonstrates how to use the ``accepts`` and ``returns``
decorators in the classes. Please pay attention to the method ``connect`` of
the class ``SqlDriver``. In these classes we're using the ``accepts``
decorator to validate keyword arguments.

.. code-block:: python

    from pyvalid import accepts, returns
    from collections.abc import Iterable


    class SqlDriver(object):

        @returns(bool)
        @accepts(object, host=str, port=int, usr=str, pwd=str, db=[str, None])
        def connect(self, **kwargs):
            conn_req = 'tsql -S {host} -p {port} -U {usr} -P {pwd} -D {db}'
            conn_req = conn_req.format(**kwargs)
            try:
                print('Establishing connection: "{}"'.format(conn_req))
                # Some code, which may cause the ConnectionError
                return True
            except ConnectionError:
                return False

        @returns(bool)
        def close(self):
            try:
                print('Closing connection')
                # Some code, which may cause the ConnectionError
                return True
            except ConnectionError:
                return False

        @returns(None, dict)
        @accepts(object, str, Iterable)
        def query(self, sql, params=None):
            try:
                if params is not None:
                    sql = sql.format(*params)
                query_info = 'Processing request "{}"'.format(sql)
                print(query_info)
                return dict()
                # Some code, which may cause the ConnectionError
            except ConnectionError:
                return None


    sql_driver = SqlDriver()

    conn_params = {
        'host': '8.8.8.8',
        'port': 1433,
        'usr': 'admin',
        'pwd': 'password',
        'db': 'wiki'
    }
    sql_driver.connect(**conn_params)

    sql = 'SELECT * FROM ProgrammingLang'
    pl = sql_driver.query(sql)

    sql = 'SELECT * FROM ProgrammingLang WHERE name={}'
    python_pl = sql_driver.query(sql, ('Python',))

    sql_driver.close()


When we need a bit more complex validators, we may use built-in ``pyvalid`
validators available in the ``pyvalid.validators`` module.
For example, here we're using the ``StringValidator`` validator based on the
regular expression and the ``NumberValidator`` based on the min/max allowed
values:

.. code-block:: python

    from pyvalid import accepts, returns
    from pyvalid.validators import NumberValidator, StringValidator

    @accepts(StringValidator(re_pattern=r'^[A-Za-z]+\s?[A-Za-z]+\s?[A-Za-z]+$'))
    @returns(NumberValidator(min_val=0, max_val=10))
    def get_review(name):
        message = 'Hello, {}! Please review our application from 0 to 10.'
        print(message.format(name))
        return float(input())

    review = get_review('Elon Musk')
    print(review)
    # Will raise the InvalidReturnTypeError exception only if user enter
    # the value, which is not in the [0, 10] range.

    another_review = get_review('Elon Musk 2')
    # Raises the ArgumentValidationError exception, since the "Elon Musk 2"
    # value doesn't match the pattern.


The example below explains how to use the custom validator. It's pretty
easy actually, we just need to apply the ``pyvalid.validators.is_validator``
decorator to the validation function.

.. code-block:: python

    from pyvalid import accepts
    from pyvalid.validators import is_validator


    class User(object):

        registered_users = list()

        class Validator(object):

            unsafe_passwords = [
                '111111', '000000', '123123',
                '123456', '12345678', '1234567890',
                'qwerty', 'sunshine', 'password',
            ]

            @classmethod
            @is_validator
            def login_checker(cls, login):
                if isinstance(login, str) and 1 <= len(login) <= 16:
                    for reg_user in User.registered_users:
                        if login == reg_user.login:
                            return False
                return True

            @classmethod
            @is_validator
            def password_checker(cls, password):
                return (
                    isinstance(password, str)
                    and
                    6 <= len(password) <= 32
                    and
                    password not in cls.unsafe_passwords
                )

        def __init__(self, login, password):
            self.__login = None
            self.login = login
            self.__password = None
            self.password = password
            User.registered_users.append(self)

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


    user = User('admin', 'Str0ng_P@ssw0rd!')

    print(user.login, user.password)
    # Outputs: "admin Str0ng_P@ssw0rd!"

    user.password = 'qwerty'
    # Raises the ArgumentValidationError exception, because the 
    # User.Validator.password_checker method returns False.

    user = User('admin', 'An0ther_Str0ng_P@ssw0rd!')
    # Raises the ArgumentValidationError exception, because the
    # User.Validator.login_checker method returns False.

