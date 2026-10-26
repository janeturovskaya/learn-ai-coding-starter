import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("7 / 2", "3"),
        ("2 - 3 * 4", "-10"),
        ("(2 - 3) * 4", "-4"),
        ("--5", "5"),
        ("“ab” + “cd”", "abcd"),
    ],
)
def test_arithmetic(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (7, 2, 3),
        (-7, 2, -3),
        (7, -2, -3),
        (-7, -2, 3),
        (-6, 2, -3),
        (6, -2, -3),
        (-6, -2, 3),
        (-1, 2, 0),
        (1, -2, 0),
        (0, 2, 0),
        (0, -2, 0),
        (-9007199254740995, 2, -4503599627370497),
        (9007199254740995, -2, -4503599627370497),
    ],
)
def test_division_truncates_toward_zero(left: int, right: int, expected: int):
    assert run(f"hallucinate({left} / {right})✨") == f"{expected}\n"


@pytest.mark.parametrize("left_sign", [-1, 1])
@pytest.mark.parametrize("right_sign", [-1, 1])
def test_division_preserves_arbitrary_precision(left_sign: int, right_sign: int):
    left = left_sign * (10**400 + 1)
    right = right_sign * 2
    expected = left_sign * right_sign * (10**400 // 2)
    assert run(f"hallucinate({left} / {right})✨") == f"{expected}\n"


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 == 1", "✅"),
        ("✅ == 1", "❌"),  # Python would say True == 1
        ("❌ == 0", "❌"),
        ("“1” == 1", "❌"),
        ("nothing() == nothing()", "✅"),  # nil == nil
        ("nothing() == ❌", "❌"),
        ("nothing == nothing", "✅"),
        ("nothing != hallucinate", "✅"),
    ],
)
def test_equality_never_coerces(expression: str, expected: str):
    source = f"clanker nothing() {{ }}\nhallucinate({expression})✨"
    assert run(source) == f"{expected}\n"


def test_short_circuit_skips_right_operand():
    assert run("hallucinate(❌ && 1 / 0 == 0)✨\nhallucinate(✅ || 1 / 0 == 0)✨") == "❌\n✅\n"


def test_logical_operands_must_be_booleans():
    assert fails("hallucinate(1 && ✅)✨") == (
        "SlopLang runtime error at line 1: left operand of '&&' must be a boolean, got number"
    )
    assert fails("hallucinate(✅ && 1)✨") == (
        "SlopLang runtime error at line 1: right operand of '&&' must be a boolean, got number"
    )


def test_assignment_walks_up_the_scope_chain():
    source = """slop x = 1✨
{
    {
        x = 2✨
    }
}
hallucinate(x)✨"""
    assert run(source) == "2\n"


def test_loadbearing_can_be_read_while_slop_can_be_reassigned():
    source = """loadbearing LIMIT = 100✨
slop score = 10✨
score = score + 1✨
hallucinate(LIMIT + score)✨"""
    assert run(source) == "111\n"


def test_loadbearing_initializer_can_be_an_expression():
    source = """slop score = 10✨
loadbearing LIMIT = score * 2✨
score = 30✨
hallucinate(LIMIT)✨"""
    assert run(source) == "20\n"


def test_loadbearing_assignment_errors_only_when_executed():
    source = """loadbearing LIMIT = 100✨
vibe ❌ {
    LIMIT = 200✨
}
clanker never_called() {
    LIMIT = 300✨
}
hallucinate(LIMIT)✨"""
    assert run(source) == "100\n"


@pytest.mark.parametrize("outer", ["slop", "loadbearing"])
@pytest.mark.parametrize("inner", ["slop", "loadbearing"])
def test_declarations_can_shadow_outer_bindings(outer: str, inner: str):
    source = f"""{outer} value = 100✨
{{
    {inner} value = 10✨
    hallucinate(value)✨
}}
hallucinate(value)✨"""
    assert run(source) == "10\n100\n"


def test_assignment_updates_nearest_mutable_shadow_not_outer_loadbearing():
    source = """loadbearing LIMIT = 100✨
{
    slop LIMIT = 10✨
    {
        LIMIT = 20✨
    }
    hallucinate(LIMIT)✨
}
hallucinate(LIMIT)✨"""
    assert run(source) == "20\n100\n"


def test_loadbearing_can_be_declared_in_a_function():
    source = """clanker limit(n) {
    loadbearing LIMIT = n + 1✨
    ship LIMIT✨
}
hallucinate(limit(99))✨"""
    assert run(source) == "100\n"


def test_loop_body_is_a_fresh_scope_each_iteration():
    source = """slop i = 0✨
ralph i < 3 {
    slop j = i * 10✨
    i = i + 1✨
}
hallucinate(i)✨"""
    assert run(source) == "3\n"


def test_function_locals_do_not_leak_and_globals_are_visible():
    source = """slop total = 0✨
clanker add(n) {
    slop doubled = n * 2✨
    total = total + doubled✨
}
add(5)✨
hallucinate(total)✨
hallucinate(doubled)✨"""
    result = run_source(source)
    assert result.stdout == "10\n"
    assert result.stderr == "SlopLang runtime error at line 8: undefined variable 'doubled'\n"


def test_parameters_are_local_and_mutable():
    source = """slop n = 1✨
clanker bump(n) {
    n = n + 100✨
    ship n✨
}
hallucinate(bump(5))✨
hallucinate(n)✨"""
    assert run(source) == "105\n1\n"


def test_ship_unwinds_nested_blocks_and_loops():
    source = """clanker find() {
    slop i = 0✨
    ralph ✅ {
        vibe i == 3 {
            ship i✨
        }
        i = i + 1✨
    }
}
hallucinate(find())✨"""
    assert run(source) == "3\n"


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("hallucinate(-“a”)✨", "operand of unary '-' must be a number, got string"),
        ("hallucinate(“a” < “b”)✨", "operands of '<' must be numbers, got string and string"),
        ("hallucinate(1 - ✅)✨", "operands of '-' must be numbers, got number and boolean"),
        ("ralph 0 { }", "ralph condition must be a boolean, got number"),
        ("hallucinate(1)(2)✨", "can only call clankers, got nil"),
    ],
)
def test_runtime_type_errors(source: str, message: str):
    assert fails(source) == f"SlopLang runtime error at line 1: {message}"


def test_stringify_every_value_kind():
    source = """clanker f() { }
hallucinate(0)✨
hallucinate(-42)✨
hallucinate(“str”)✨
hallucinate(✅)✨
hallucinate(❌)✨
hallucinate(f())✨
hallucinate(f)✨
hallucinate(hallucinate)✨"""
    assert run(source) == "0\n-42\nstr\n✅\n❌\nnil\n<clanker f>\n<clanker hallucinate>\n"


def test_hallucinate_accepts_zero_one_or_many_arguments():
    source = """clanker f() { }
hallucinate()✨
hallucinate(“hello”)✨
hallucinate(1, “two”, ✅, ❌, f(), f, hallucinate)✨
hallucinate(hallucinate())✨"""
    assert run(source) == "\nhello\n1 two ✅ ❌ nil <clanker f> <clanker hallucinate>\n\nnil\n"


def test_hallucinate_evaluates_arguments_left_to_right():
    source = """clanker next() {
    hallucinate(“evaluated”)✨
    ship 42✨
}
hallucinate(next(), next())✨"""
    assert run(source) == "evaluated\nevaluated\n42 42\n"


def test_variation_selector_after_emoji_is_accepted():
    assert run("hallucinate(✅️)✨️\nhallucinate(❌️)✨️") == "✅\n❌\n"


def test_mutual_recursion():
    source = """clanker is_even(n) {
    vibe n == 0 {
        ship ✅✨
    }
    ship is_odd(n - 1)✨
}
clanker is_odd(n) {
    vibe n == 0 {
        ship ❌✨
    }
    ship is_even(n - 1)✨
}
hallucinate(is_even(10))✨
hallucinate(is_odd(7))✨
hallucinate(is_even(7))✨"""
    assert run(source) == "✅\n✅\n❌\n"


def test_functions_are_first_class_values():
    source = """clanker twice(x) {
    ship x * 2✨
}
slop f = twice✨
hallucinate(f(21))✨
hallucinate(f == twice)✨
hallucinate(f == hallucinate)✨"""
    assert run(source) == "42\n✅\n❌\n"


def test_recursion_below_the_cap_works():
    source = """clanker down(n) {
    vibe n == 0 {
        ship 0✨
    }
    ship 1 + down(n - 1)✨
}
hallucinate(down(400))✨"""
    assert run(source) == "400\n"


def test_numbers_are_arbitrary_precision():
    source = """slop n = 1✨
slop i = 0✨
ralph i < 100 {
    n = n * 2✨
    i = i + 1✨
}
hallucinate(n)✨"""
    assert run(source) == "1267650600228229401496703205376\n"


def test_empty_program_produces_nothing():
    result = run_source("— nothing but a comment\n")
    assert (result.stdout, result.stderr, result.exit_code) == ("", "", 0)
