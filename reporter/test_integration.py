from pathlib import Path

import pytest

from csv_ import CSV
from reporter import DepartmentsReporter, Employee

# Test data for CSV files
CSV_CONTENT_1 = """id,name,department,hours_worked,hourly_rate
1,John Doe,Engineering,40,50
2,Jane Smith,Engineering,35,45
"""


def test_csv_to_report_integration(tmp_path: Path):
    file_path = tmp_path / "test.csv"
    file_path.write_text(CSV_CONTENT_1, encoding="UTF-8")

    employees = []
    with CSV(str(file_path)) as csv:
        for row in csv.get_rows():
            employees.append(Employee.from_dict(row))

    reporter = DepartmentsReporter(employees)
    report = reporter.create_payout_report()

    assert "Engineering" in report
    assert len(report["Engineering"]) == 2
    assert report.total_values["Engineering"] == {"hours": 75, "payout": 3575}
