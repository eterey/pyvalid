# pyvalid

Python validation tool, which used for checking of input function parameters and return values.
Module consists just from two decorators: `accepts` and `returns`.


#### `accepts(*accepted_arg_values)`
A decorator to validate a types and values of input parameters for a given function.
You can pass the set of accepted types and values as a input decorator's parameters.
Validation process can raise the following exceptions:

* `pyvalid.InvalidArgumentNumberError` -- when the number or position of arguments supplied to a function is incorrect.
* `pyvalid.ArgumentValidationError` -- when the type of an argument to a function is not what it should be.


#### `returns(*accepted_returns_values)`
A decorator to validate the returns value of a given function.
You can pass the set of accepted types and values as a input decorator's parameters.
Validation process can raise InvalidReturnType in situation, when the return value is not in collection of supported values and types.


### Example of usage

Function `calc` in example below has next limitations:
* Can return only `int` or `float` value;
* First parameter must be only in `str` type;
* Second parameter must be in `int` value or equals to `2.0`;
* Third parameter must be in `int` or `float` type.

```
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
# because returns value is in str type.
print(calc('*', 2, 3, '"4"'))
```

Here is an example of usage `pyvalid` module in context of classes.

```
from pyvalid import accepts, returns
from collections import Iterable

class SqlDriver(object):

    @returns(bool)
    @accepts(object, str, int, str, str, str)
    def connect(self, host, port, user, password, database):
        return True

    @returns(bool)
    def close(self):
        return True

    @returns(None, dict)
    @accepts(object, str, Iterable)
    def query(self, sql, params=None):
        return None

sql_driver = SqlDriver()

sql_driver.connect('8.8.8.8', 1433, 'admin', 'password', 'programming')

sql = r'SELECT * FROM ProgrammingLang'
pl = sql_driver.query(sql)

sql = r'SELECT * FROM ProgrammingLang WHERE name=?'
python_pl = sql_driver.query(sql, ('Python',))

sql_driver.close()
```

# How to install

```pip install -U pyvalid```
