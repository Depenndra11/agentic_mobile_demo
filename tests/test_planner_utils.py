"""
Unit tests for Planner's pure helper functions.

These are @staticmethod on purpose so they can be tested without
instantiating Planner (which requires a GEMINI_API_KEY at import time).
"""

from agents.planner import Planner


def test_remove_duplicates_keeps_first_occurrence_case_insensitive():
    testcases = [
        {"scenario": "Valid login"},
        {"scenario": "valid login"},   # duplicate, different case
        {"scenario": "Invalid password"},
    ]

    result = Planner.remove_duplicates(testcases)

    assert len(result) == 2
    assert result[0]["scenario"] == "Valid login"
    assert result[1]["scenario"] == "Invalid password"


def test_remove_duplicates_handles_missing_scenario_key():
    testcases = [{}, {}]

    result = Planner.remove_duplicates(testcases)

    # both have "" as scenario -> treated as duplicates of each other
    assert len(result) == 1


def test_assign_ids_produces_zero_padded_sequential_ids():
    testcases = [{"scenario": "a"}, {"scenario": "b"}, {"scenario": "c"}]

    result = Planner.assign_ids(testcases)

    assert [tc["id"] for tc in result] == ["TC01", "TC02", "TC03"]


def test_format_value_handles_none_list_dict_and_scalars():
    assert Planner.format_value(None) == ""
    assert Planner.format_value(["a", "b"]) == "a\nb"
    assert Planner.format_value({"k": "v"}) == '{\n  "k": "v"\n}'
    assert Planner.format_value(5) == "5"
