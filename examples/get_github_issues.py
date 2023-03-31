import typing
import datetime

from pseudocode import pseudo_function

@pseudo_function(review=True)
def get_issues(respository: str) -> typing.List[typing.Tuple[str, int, datetime.datetime]]:
    """A function to fetch all issues created by

    A function that does the following:
     - assume you have a github token environment variable GITHUB_TOKEN
     - assume that repositiory is of the form organization/repo
     - use the requests library
     - fetch all github issues from repository in last 10 days
     - only show issue numbers which are odd
     - return a tuple with issue titles, number, and date created

    Examples
    --------
    >>> all([_[1] % 2 == 1 for _ in get_issues("conda/conda")])
    True
    """
    pass


print('github issues', get_issues("conda/conda"))
