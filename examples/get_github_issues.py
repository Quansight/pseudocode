import typing

from pseudocode import pseudo_function

@pseudo_function
def get_issues(respository: str) -> typing.List[int]:
    """A function to fetch all issues created by

    A function that does the following:
     - assume you have a github token environment variable GITHUB_TOKEN
     - assume that repositiory is of the form organization/repo
     - use the requests library
     - fetch all github issues from repository in last 10 days
     - only show issue numbers with are odd
     - return the issue titles

    Examples
    --------
    >>> get_issues("conda/conda")
    """
    pass


print('github issues', get_issues("conda/conda"))
