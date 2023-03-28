# PseudoCode

`pseudocode` is a python module which allows users to describe the
functions they want without writing the actual code. It empowers users
to iterate with [large language
models](https://en.wikipedia.org/wiki/Large_language_model) to
generate functions which satisfy the users along with defined tests.

```python
from pseudocode import pseudo_function

@pseudo_function
def my_sum_func(a: int, b: int, c: int) -> str:
    """A function which adds all arguments together and multiplies by two

    Examples
    --------
    >>> my_sum_func(1, 2, 3)
    6
    """
    pass

my_sum_func(1, 4, 5) # LLM generated function
```

This work uses OpenAIs `gpt-3.5-turbo` at the moment. Because of this
it expects an environment variable `OPENAI_API_KEY` to be defined.

