import pytest

from utils.paginator import Paginator


def make_paginator(items, page=1, per_page=1):
    return Paginator(items, page=page, per_page=per_page)


def test_empty_list_has_zero_pages():
    p = make_paginator([])
    assert p.pages == 0
    assert p.len == 0


def test_single_item_single_page():
    p = make_paginator(["a"])
    assert p.pages == 1
    assert p.len == 1


def test_pages_calculated_correctly():
    p = make_paginator(list(range(10)), per_page=3)
    assert p.pages == 4


def test_exact_division_gives_correct_pages():
    p = make_paginator(list(range(6)), per_page=3)
    assert p.pages == 2


def test_get_page_returns_first_item():
    p = make_paginator(["x", "y", "z"], page=1)
    assert p.get_page() == ["x"]


def test_get_page_returns_correct_slice_per_page():
    p = make_paginator(list(range(9)), page=2, per_page=3)
    assert p.get_page() == [3, 4, 5]


def test_get_page_last_page_partial():
    p = make_paginator(list(range(5)), page=3, per_page=2)
    assert p.get_page() == [4]


def test_get_page_empty_list_returns_empty():
    p = make_paginator([], page=1)
    assert p.get_page() == []


def test_has_next_on_first_of_many():
    p = make_paginator(list(range(3)), page=1)
    assert p.has_next() == 2


def test_has_next_false_on_last_page():
    p = make_paginator(list(range(3)), page=3)
    assert p.has_next() is False


def test_has_previous_on_second_page():
    p = make_paginator(list(range(3)), page=2)
    assert p.has_previous() == 1


def test_has_previous_false_on_first_page():
    p = make_paginator(list(range(3)), page=1)
    assert p.has_previous() is False


def test_get_next_advances_page():
    p = make_paginator(["a", "b", "c"], page=1)
    result = p.get_next()
    assert result == ["b"]
    assert p.page == 2


def test_get_previous_retreats_page():
    p = make_paginator(["a", "b", "c"], page=3)
    result = p.get_previous()
    assert result == ["b"]
    assert p.page == 2


def test_get_next_raises_on_last_page():
    p = make_paginator(["a"], page=1)
    with pytest.raises(IndexError):
        p.get_next()


def test_get_previous_raises_on_first_page():
    p = make_paginator(["a"], page=1)
    with pytest.raises(IndexError):
        p.get_previous()


def test_paginator_works_with_tuple():
    p = Paginator((10, 20, 30), page=2)
    assert p.get_page() == (20,)