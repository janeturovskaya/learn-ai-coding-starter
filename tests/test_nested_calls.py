from sloperator.runner import run_source


def test_call_used_directly_as_another_calls_argument():
    source = """clanker double(value) {
    ship value * 2✨
}
clanker add(left, right) {
    ship left + right✨
}
hallucinate(add(double(3), 4))✨"""

    result = run_source(source)
    assert (result.stdout, result.stderr, result.exit_code) == ("10\n", "", 0)
