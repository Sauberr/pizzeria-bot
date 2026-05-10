import pytest

from utils.phone_formatting import format_phone_number


@pytest.mark.parametrize("raw", [
    "+380991234567",
    "+38 099 123 45 67",
    "0991234567",
    "380991234567",
])
def test_valid_ukraine_numbers_are_formatted(raw):
    result = format_phone_number(raw)
    assert result is not None
    assert result.startswith("+")


def test_valid_russian_number():
    result = format_phone_number("+79161234567")
    assert result is not None


def test_formatted_result_contains_country_code():
    result = format_phone_number("+380991234567")
    assert "+380" in result


def test_valid_number_stripped_of_spaces():
    result = format_phone_number("+380 99 123 45 67")
    assert " " not in result.replace(" ", "")


@pytest.mark.parametrize("raw", [
    "123",
    "abcdefghij",
    "",
    "not-a-phone",
    "00000000000",
])
def test_invalid_numbers_return_none(raw):
    assert format_phone_number(raw) is None


def test_too_short_number_returns_none():
    assert format_phone_number("123456") is None


def test_letters_mixed_with_digits_returns_none():
    assert format_phone_number("+380abc12345") is None