import pytest
from llm_output_polisher import Polisher


def test_format_only_normalizes_markdown():
    assert Polisher.format_only("###heading\r\n\r\n\r\n• item  ") == "### heading\n\n- item"


def test_empty_input():
    assert Polisher.format_only("  ") == ""


def test_invalid_type():
    with pytest.raises(TypeError):
        Polisher.format_only(None)


def test_unknown_profile_without_model_call():
    polisher = Polisher.__new__(Polisher)
    with pytest.raises(ValueError):
        polisher.polish("hello", profile="made-up")
