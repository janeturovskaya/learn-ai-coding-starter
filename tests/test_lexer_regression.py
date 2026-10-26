import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


def test_lexical_error_after_comment_reports_correct_line():
    with pytest.raises(LexicalError) as info:
        tokenize("— comment\n@")

    assert info.value.line == 2
    assert info.value.message == "unexpected character '@'"
