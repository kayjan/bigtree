import pytest

from bigtree.utils import groot


def test_whoami():
    assert groot.whoami() == "I am Groot!"


@pytest.mark.parametrize(
    ["sentence", "expected_output"],
    [("Hi!", "I am Groot!"), ("Hi there!", "I am Groot! I am Groot!")],
)
def test_speak_like_groot(sentence, expected_output):
    assert groot.speak_like_groot(sentence) == expected_output
