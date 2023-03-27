from pseudocode import pseudo_function

import pandas

@pseudo_function(review=True)
def download_titanic_df() -> pandas.DataFrame:
    """A function that downloads the titanic dataset

    Examples
    --------
    >>> download_titanic_df()
    """
    pass


print('download titanic df', download_titanic_df())
