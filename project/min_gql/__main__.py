import sys

from project.min_gql.interpreter.mingql import interpreter
from project.min_gql.interpreter.exceptions import RunTimeException


def main(*argv):
    try:
        interpreter(*argv)
    except RunTimeException as e:
        sys.stdout.write(f"Error: {e.msg}\n")
        exit(1)
    exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
