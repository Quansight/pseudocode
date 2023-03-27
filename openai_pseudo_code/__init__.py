import functools
import typing
import re
import enum

import docstring_parser
import openai
import pydantic

from rich.console import Console
from rich.syntax import Syntax
from rich.prompt import Prompt
from rich.panel import Panel
console = Console()


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


def function_description_to_openai_message(func):
    doc = docstring_parser.parse(func.__doc__)
    input_params = []
    for param in doc.params:
        input_params.append(f' - variable "{param.arg_name}" of python type "{param.type_name}"\n')

    message = OpenAIMessage(
        role=OpenAIRole.USER,
        content=f'''
A short description of what this function should do "{doc.short_description}".
A longer more detailed description of what this function should do is as follows {doc.long_description}.
This function must take as input the following python variables defined as:
{', '.join(input_params)}
This function must return a result of python type "{doc.returns.type_name}. Can you output the code?
''')

    test_cases = []
    for example in doc.examples:
        code = example.snippet.replace(func.__name__, 'run')[len('>>> '):]
        test_cases.append((f'result = str({code})', example.description))

    return message, test_cases


def openai_create_python_function_from_messages(messages: typing.List[OpenAIMessage], review: bool = True):
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[_.dict() for _ in messages])
    response_text = response.choices[0].message.content
    messages.append(OpenAIMessage(
        role=OpenAIRole.ASSISTANT,
        content=response_text,
    ))

    match = re.search('```(?:python)?(.*)```', response_text, re.DOTALL)
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


def generate_python_function_from_description(f):
    max_attempts = 5
    messages, test_cases = generate_initial_openai_messages(f)
    for attempt in range(max_attempts):
        try:
            generated_func = openai_create_python_function_from_messages(messages)
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
            messages.append(OpenAIMessage(
                role=OpenAIRole.USER,
                content=e.args[0],
            ))
    return generated_func



def pseudo_code(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        generated_func = generate_python_function_from_description(f)
        return generated_func(*args, **kwargs)
    return wrapper
