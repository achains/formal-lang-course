class RunTimeException(Exception):
    """
    Base exception for Interpreter
    """

    def __init__(self, msg: str):
        self.msg = msg


class ScriptPathException(RunTimeException):
    """
    Raises when failed to open given script
    """

    def __init__(self, filename: str):
        self.msg = f"Could not open {filename}"


class ScriptExtensionException(RunTimeException):
    """
    Raises when given script doesn't have .gql extension
    """

    def __init__(self):
        self.msg = f"Script name doesn't match *.gql"


class LoadGraphException(RunTimeException):
    """
    Raises when failed to load graph
    (usually by load_graph instruction)
    """

    def __init__(self, name: str):
        self.msg = f"Could not open graph '{name}'. Check correctness of given name"


class ConversionException(RunTimeException):
    """
    Raises when there is no viable conversion between two given types
    """

    def __init__(self, lhs: str, rhs: str):
        self.msg = f"conversion error"


class NotImplementedException(RunTimeException):
    """
    Raises when evaluated instruction has not yet implemented
    """

    def __init__(self, instruction):
        self.msg = f"{instruction} is not implemented"


class VariableNotFoundException(RunTimeException):
    """
    Raises if variable is not found in Memory object
    """

    def __init__(self, name: str):
        self.msg = f"Variable name '{name}' is not defined"


class GQLTypeError(RunTimeException):
    """
    Raises if expected and actual types differ
    """

    pass
