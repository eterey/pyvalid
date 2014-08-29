pyvalid
-------

Python validation tool, which is used for checking function's input parameters and return values.
Module consists of two decorators: `accepts` and `returns`.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`accepts(*accepted_arg_values, **accepted_kwargs_values)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A decorator for validating types and values of input parameters of a given function.
You can pass the set of accepted types and values as decorator's input parameters.
Validation process can raise the following exceptions:

* `pyvalid.InvalidArgumentNumberError` — when the number or position of arguments supplied to a function is incorrect.
* `pyvalid.ArgumentValidationError` — when the type of an argument to a function is not what it should be.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`returns(*accepted_returns_values)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A decorator for validating the return value of a given function.
You can pass the set of accepted types and values as a decorator's input parameters.
Validation process can raise `pyvalid.InvalidReturnType` when the return value is not in the collection of supported values and types.


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


    # Returns int value: 24.
    print(calc('*', 2, 3, 4))

    # Returns float value: 24.0.
    print(calc(operator='*', val1=2, val2=3.0, val3=4))

    # Returns float value: 24.0.
    print(calc('*', 2.0, 3, 4))

    # Raise pyvalid.ArgumentValidationError exception,
    # because second argument has unsupported value.
    print(calc('*', 3.14, 3, 4))


    # Raise pyvalid.InvalidReturnType exception,
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

