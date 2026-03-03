"""
WARNING — PLEASE READ

This file exists **solely** to satisfy submit50's strict requirements.
It contains a small collection of simplified, self-contained functions,
extracted and adapted from the real project codebase.

⚠️ These functions DO NOT represent the actual architecture of the project.
The real application is significantly more complex and is driven by the
main() functions located in dbf_parser.py and app.py, along with multiple
supporting modules.

This project.py file is therefore a lightweight compatibility layer created
only so that pytest and submit50 can evaluate the required functions
in isolation.

Have a nice day!
"""


from project import (
    normalize_field,
    normalize_codart,
    calc_giacenza,
    build_condition,
    choose_ubicazione
)


def test_normalize_field():
    assert normalize_field("  a,b\nc ") == "a.b c"
    assert normalize_field(None) == ""
    assert normalize_field("x\ny") == "x y"


def test_normalize_codart():
    result = normalize_codart(" ABC ")
    assert result.startswith("ABC")
    assert len(result) == 25
    assert normalize_codart("12,5").startswith("12.5")


def test_calc_giacenza():
    assert calc_giacenza(10, 5, 0, 3, 2) == 10
    assert calc_giacenza("1", "2", "3", "4", "5") == -3
    assert calc_giacenza(None, 1, 1, 1, 1) == 0.0
    assert calc_giacenza("ciao", 1, 1, 1, 1) == 0.0  # ValueError
    assert calc_giacenza(None, None, None, None, None) == 0.0  # TypeError
    assert calc_giacenza({}, [], (), "x", True) == 0.0


def test_build_condition():
    # exact
    assert build_condition("codart", exact_value="ABC") == "codart = 'ABC'"
    # between
    assert build_condition("data", min_value="2023-01-01", max_value="2023-01-31") == "data BETWEEN '2023-01-01' AND '2023-01-31'"
    # min only
    assert build_condition("prezzo", min_value="10,0") == "prezzo >= '10.0'"
    # max only
    assert build_condition("prezzo", max_value="99,99") == "prezzo <= '99.99'"
    # exact overrides range
    assert build_condition("codart", exact_value="XYZ", min_value="AAA", max_value="ZZZ") == "codart = 'XYZ'"
    # nothing provided
    assert build_condition("peso") is None


def test_choose_ubicazione():
    assert choose_ubicazione(None, "A1", False) == "A1"
    assert choose_ubicazione("", "B2", False) == "B2"
    assert choose_ubicazione("A1", "B2", False) == "A1"
    assert choose_ubicazione("A1", "B2", True) == "B2"
