import functools
import typing
import re
import enum
import inspect

import docstring_parser
import openai
import pydantic

from rich.console import Console
from rich.syntax import Syntax
from rich.prompt import Prompt
from rich.panel import Panel
console = Console()


__version__ = "0.0.1"


class OpenAIException(Exception):
    pass


class OpenAIRole(enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class OpenAIMessage(pydantic.BaseModel):
    role: OpenAIRole
    content: str

    class Config:
        use_enum_values = True


def generate_initial_openai_messages(func: typing.Callable):
    message, test_cases = function_description_to_openai_message(func)
    messages = [
        OpenAIMessage(
            role=OpenAIRole.SYSTEM,
            content="""
You are a helpful assistant which only outputs python code in response to questions with no additional text.
You always return a python function named run within code blocks ```python ... ```.
Do not include docstrings or type annotations with the function.
"""
        ),
        message,
    ]
    return messages, test_cases


def function_description_to_openai_message(func: typing.Callable):
    doc = docstring_parser.parse(func.__doc__)

    function_description = f"""
The following is a short description of what this function should do "{doc.short_description}".
A longer more detailed description of what this function should do is as follows:
{doc.long_description}
The function takes the following arguments:
"""

    func_type_hints = typing.get_type_hints(func)
    for arg_name in inspect.signature(func).parameters:
        param_description = f' - variable "{arg_name}"'
        if arg_name in func_type_hints:
            param_description += f' of python type "{str(func_type_hints[arg_name])}"'
        function_description += param_description + "\n"

    if 'return' in func_type_hints:
        function_description += f'This function must return a result of python type "{str(func_type_hints["return"])}".'

    function_description += "\nOutput code that will satisfy the given requirments."
    message = OpenAIMessage(
        role=OpenAIRole.USER,
        content=function_description
    )

    test_cases = []
    for example in doc.examples:
        code = example.snippet.replace(func.__name__, 'run')[len('>>> '):]
        test_cases.append((f'result = str({code})', example.description))

    return message, test_cases


def openai_create_python_function_from_messages(messages: typing.List[OpenAIMessage], review: bool = False):
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[_.dict() for _ in messages])
    response_text = response.choices[0].message.content
    messages.append(OpenAIMessage(
        role=OpenAIRole.ASSISTANT,
        content=response_text,
    ))

    match = re.search('```python(.*)```', response_text, re.DOTALL)
    if match is None:
        raise OpenAIException("Your response must be wrapped in ```python ... ```")

    code = match.group(1)
    console.print(Panel(Syntax(code, "python"), title="Code Review"))
    if review:
        feedback = Prompt.ask("What code feedback would you like to provide? (leave empty for approval)")
        if feedback:
            raise OpenAIException(feedback)
    else:
        console.print("Code review disabled and code auto approved to run")

    try:
        state = {}
        exec(code, state, state)
    except Exception as e:
        raise OpenAIException(f"I ran into an exeption when I tried to execte the code you supplied. Could you try an fix it? Here is the exception {e}")

    if 'run' not in state:
        raise OpenAIException("Your response did not include a python function named run. Could you try to fix this?")

    return state['run']


def generate_python_function_from_description(func: typing.Callable, max_attempts: int = 5, review: bool = False):
    messages, test_cases = generate_initial_openai_messages(func)
    for attempt in range(max_attempts):
        try:
            generated_func = openai_create_python_function_from_messages(messages, review=review)
            for test_case, result in test_cases:
                state = {'run': generated_func}
                try:
                    exec(test_case, state, state)
                except Exception as e:
                    raise OpenAIException(f'The following python test case `{test_case} == {result}` failed and raised an exception. The exception was of type {type(e)} and the brief exception message was {e}')

                if result and state['result'] != result:
                    console.print(f"[bold]fail[/bold] {test_case}!={result}", style="red")
                    raise OpenAIException(f'The following python test case `{test_case} == {result}` failed and gave the wrong result of "{state["result"]}"')
                else:
                    console.print(f"[bold]pass[/bold] {test_case}=={state['result']}", style="green")
            break
        except OpenAIException as e:
            console.print(e.args[0], style="red")
            messages.append(OpenAIMessage(
                role=OpenAIRole.USER,
                content=e.args[0],
            ))
    else:
        message = f'failed to generate function in {max_attempts} attemps'
        console.print(message, style="red")
        raise Exception(message)
    return generated_func


def pseudo_function(func: typing.Callable = None, review: bool = False):
    if func is None:
        return lambda func: pseudo_function(func=func, review=review)

    generated_func = generate_python_function_from_description(func, review=review)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return generated_func(*args, **kwargs)
    return wrapper
