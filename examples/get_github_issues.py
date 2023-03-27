import typing

from openai_pseudo_code import pseudo_code

@pseudo_code
def get_issues(respository: str) -> typing.List[int]:
    """A function to fetch all issues created by

    A function that does the following:
     - assume you have a github token environment variable GITHUB_TOKEN
     - assume that repositiory is of the form organization/repo
     - use the requests library
     - fetch all github issues from repository in last 10 days
     - only show issue numbers with are odd
     - return the issue first 10 characters

    Parameters
    ----------
    repository: str

    Returns
    -------
    list[str]

    Examples
    --------
    >>> get_issues("conda/conda")
    """
    pass


print('github issues', get_issues("conda/conda"))
