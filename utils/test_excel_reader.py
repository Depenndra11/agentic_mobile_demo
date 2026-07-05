from openpyxl import Workbook

from utils.excel_reader import ExcelReader


def _make_excel(tmp_path, rows):
    wb = Workbook()
    ws = wb.active
    ws.append(["ID", "Scenario", "Execution Type"])
    for row in rows:
        ws.append(row)

    path = tmp_path / "testcases.xlsx"
    wb.save(path)
    return path


def test_get_testcases_returns_all_rows_without_filter(tmp_path):
    path = _make_excel(tmp_path, [
        ["TC01", "Valid login", "Automated"],
        ["TC02", "Invalid login", "Manual"],
    ])

    testcases = ExcelReader(path).get_testcases()

    assert len(testcases) == 2
    assert testcases[0]["ID"] == "TC01"


def test_get_testcases_filters_by_execution_type_case_insensitively(tmp_path):
    path = _make_excel(tmp_path, [
        ["TC01", "Valid login", "Automated"],
        ["TC02", "Invalid login", "Manual"],
    ])

    testcases = ExcelReader(path).get_testcases(execution_type="automated")

    assert len(testcases) == 1
    assert testcases[0]["ID"] == "TC01"


def test_get_testcases_does_not_crash_on_blank_execution_type(tmp_path):
    path = _make_excel(tmp_path, [
        ["TC01", "Valid login", None],  # blank cell
    ])

    # Previously this raised AttributeError: 'NoneType' object has no
    # attribute 'lower'. Should now just be filtered out cleanly.
    testcases = ExcelReader(path).get_testcases(execution_type="automated")

    assert testcases == []