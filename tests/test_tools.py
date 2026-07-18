from tools import multiply_numbers


def test_multiply_positive_numbers() -> None:
    result = multiply_numbers.invoke(
        {
            "first_number": 20,
            "second_number": 15,
        }
    )

    assert result == 300


def test_multiply_negative_numbers() -> None:
    result = multiply_numbers.invoke(
        {
            "first_number": -5,
            "second_number": 4,
        }
    )

    assert result == -20


def test_multiply_by_zero() -> None:
    result = multiply_numbers.invoke(
        {
            "first_number": 100,
            "second_number": 0,
        }
    )

    assert result == 0