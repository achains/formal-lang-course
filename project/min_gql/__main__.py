import sys

from project.min_gql.interpreter.mingql import interpreter
from project.min_gql.interpreter.exceptions import RunTimeException


def main():
    program = "".join(sys.stdin.readlines())
    try:
        interpreter(program)
        sys.stdout.write("\nEnded with exit code 0")
        return 0
    except RunTimeException as e:
        sys.stdout.write(e.msg)
        sys.stdout.write("\nEnded with exit code 1\n")
        return 1


if __name__ == "__main__":
    main()
