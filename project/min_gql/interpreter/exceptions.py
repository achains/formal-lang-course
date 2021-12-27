class RunTimeException(Exception):
    """
    Base exception for Interpreter
    """

    def __init__(self, msg: str):
        self.msg = msg


class LoadGraphException(RunTimeException):
    """
    Raises when failed to load graph
    (usually by load_graph instruction)
    """

    def __init__(self, name: str):
        self.msg = f"Can not open graph '{name}'. Check correctness of given name"


class ConversionException(RunTimeException):
    """
    Raises when there is no viable conversion between two given types
    """

    def __init__(self, lhs: str, rhs: str):
        self.msg = f""