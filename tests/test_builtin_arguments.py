from io import StringIO

from sloperator.evaluator import Interpreter
from sloperator.evaluator.values import Builtin, Value
from sloperator.lexer import tokenize
from sloperator.parser import parse


def test_builtin_receives_arguments_as_tuple():
    received: list[tuple[Value, ...]] = []

    def record(arguments: tuple[Value, ...], line: int) -> Value:
        received.append(arguments)
        return None

    interpreter = Interpreter(StringIO())
    interpreter.globals.declare("record", Builtin("record", record), False, 0)
    interpreter.run(parse(tokenize("record(1, “two”, ✅)✨")))

    assert received == [(1, "two", True)]
