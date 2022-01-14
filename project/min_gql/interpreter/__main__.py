import sys

from project.min_gql.interpreter.mingql import interpreter


def main():
    program = ''.join(sys.stdin.readlines())
    return interpreter(program)


if __name__ == '__main__':
    main()
