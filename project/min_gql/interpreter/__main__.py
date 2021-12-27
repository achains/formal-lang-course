from project.min_gql.interpreter import mingql


def main(*args, **kwargs):
    """

    Returns
    -------
    Result of interpreter evaluation
    """

    return mingql(*args, **kwargs)


if __name__ == "__main__":
    main()
