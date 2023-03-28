# PseudoCode

`pseudocode` is a python module which allows users to describe the
functions they want via type annotations and docstrings without
writing the actual code. It empowers users to iterate with [large
language models](https://en.wikipedia.org/wiki/Large_language_model)
to generate functions which satisfy the user along with defined tests.

`pseudocode` enforces the defined tests and provides automated
feedback to the LLM when attempting to run these tests by reporting
exceptions. There is a built in review cycle for the user to provide
feedback on the generated code to help guide the LLM.

[![asciicast](https://asciinema.org/a/xXpi8CX1qrL7U04m1uZPWBAiN.svg)](https://asciinema.org/a/xXpi8CX1qrL7U04m1uZPWBAiN)

```python
from pseudocode import pseudo_function

@pseudo_function(review=True)
def my_sum_func(a: int, b: int, c: int) -> str:
    """A function which adds all arguments together and multiplies by two

    Examples
    --------
    >>> my_sum_func(1, 2, 3)
    12
    """
    pass

@pseudo_function
def get_total_issues(repository: str) -> int:
    """Get the total issues of given github repository

    Examples
    --------
    >>> get_total_issues("conda/conda")
    """
    pass


# LLM generated functions!
print(my_sum_func(1, 4, 5)) 
print(get_total_issues('conda/conda-libmamba-solver'))
```

This work uses OpenAIs `gpt-3.5-turbo` at the moment. Because of this
it expects an environment variable `OPENAI_API_KEY` to be defined.

# Vision

Much like how high level languages such as `python` are abstractions
above lower level languages like `C/C++`. `psuedocode` aims to take
advantages of LLMs to work with developers and enable them to create
high level well defined interfaces. LLMs will fill in the details with
iteration and feedback from the user.

Longer terms goals:
 - `psuedocode.pseudo_file` function to generate non-python files e.g. `docker-compose.yaml`, `Dockerfile`, `pyproject.toml`, etc.
 - caching of functions generated from `pseudocode.pseudo_function`
 - richer testing utilities for defined interfaces

# License

MIT
