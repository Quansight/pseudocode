from pseudocode import pseudo_function


def test_my_add():
    @pseudo_function
    def my_add(a: int, b: int) -> str:
        """Add numbers together, then if odd subtract 2, finally multiply by two

        Examples
        --------
        >>> my_add(1, 2)
        2
        >>> my_add(10, 20)
        60
        """

    assert my_add(3, 4) == '10'
    assert my_add(4, 4) == '16'
