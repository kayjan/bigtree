import pytest

from bigtree.utils.groot import speak_like_groot, whoami


def test_whoami():
    assert whoami() == "I am Groot!"


@pytest.mark.parametrize(
    ["sentence", "expected_output"],
    [("Hi!", "I am Groot!"), ("Hi there!", "I am Groot! I am Groot!")],
)
def test_speak_like_groot(sentence, expected_output):
    assert speak_like_groot(sentence) == expected_output
