from pseudocode import pseudo_function


@pseudo_function(review=True)
def calculate_interesting_sum(a: int, b: int, c: int) -> str:
    """A creative sum function

    A function that does the following:
     - write all your code like a beginner that came from c
     - calculates the sum of a, b, c
     - multiply result by two

    Examples
    --------
    >>> calculate_interesting_sum(2, 4, 6)
    24
    >>> calculate_interesting_sum(1, 2, 1)
    8
    >>> calculate_interesting_sum(1, 2, 3)
    """
    pass


print('openai sum', calculate_interesting_sum(4, 8, 16))
