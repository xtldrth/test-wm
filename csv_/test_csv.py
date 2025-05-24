import pytest
from pathlib import Path
from csv_ import CSV

# Test data for CSV files
CSV_CONTENT_1 = """id,name,department,hours_worked,hourly_rate
1,John Doe,Engineering,40,50
2,Jane Smith,Engineering,35,45
"""

CSV_CONTENT_2 = """id,name,department,hours_worked,salary
3,Bob Johnson,Marketing,30,60
4,Alice Brown,Marketing,25,55
"""


def test_csv_context_manager(tmp_path: Path):
    file_path = tmp_path / "test.csv"
    file_path.write_text(CSV_CONTENT_1, encoding="UTF-8")

    with CSV(str(file_path)) as csv:
        assert len(csv.files) == 1
        assert not csv.files[0].closed
    assert csv.files[0].closed


def test_csv_get_rows(tmp_path: Path):
    file_path = tmp_path / "test.csv"
    file_path.write_text(CSV_CONTENT_1, encoding="UTF-8")

    with CSV(str(file_path)) as csv:
        rows = list(csv.get_rows())
        assert len(rows) == 2
        assert rows[0] == { "id": "1", "name": "John Doe",
            "department": "Engineering",
            "hours_worked": "40",
            "hourly_rate": "50",
        }
        assert rows[1] == {
            "id": "2",
            "name": "Jane Smith",
            "department": "Engineering",
            "hours_worked": "35",
            "hourly_rate": "45",
        }


def test_csv_multiple_files(tmp_path: Path):
    file1 = tmp_path / "file1.csv"
    file2 = tmp_path / "file2.csv"
    file1.write_text(CSV_CONTENT_1, encoding="UTF-8")
    file2.write_text(CSV_CONTENT_2, encoding="UTF-8")

    with CSV(str(file1), str(file2)) as csv:
        rows = list(csv.get_rows())
        assert len(rows) == 4
        assert rows[0] == {
            "id": "1", "name": "John Doe",
            "department": "Engineering",
            "hours_worked": "40",
            "hourly_rate": "50",
        }
        assert rows[3] == {
            "id": "4",
            "name": "Alice Brown",
            "department": "Marketing",
            "hours_worked": "25",
            "salary": "55",
        }
