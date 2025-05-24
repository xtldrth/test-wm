import json
from pathlib import Path

import pytest

from reporter import DepartmentsReporter, Employee, Report


def test_report_str():
    report_data = {
        "Engineering": [
            {"name": "John Doe", "hours": 40, "rate": 50, "payout": 2000},
            {"name": "Jane Smith", "hours": 35, "rate": 45, "payout": 1575},
        ]
    }
    report = Report(report_data, compute_total_for={"hours", "payout"})
    report_str = str(report)
    print(report_str)
    expected = (
        "                name          hours    rate    payout    \n"
        "Engineering\n"
        "--------------- John Doe      40       50      2000      \n"
        "--------------- Jane Smith    35       45      1575      \n"
        "                              75               3575      \n"
    )
    assert report_str == expected


def test_report_to_json_string():
    report_data = {
        "Engineering": [
            {"name": "John Doe", "hours": 40, "rate": 50, "payout": 2000},
        ]
    }
    report = Report(report_data, compute_total_for={"hours", "payout"})
    json_str = report.to_json()
    expected = {
        "Engineering": [{"name": "John Doe", "hours": 40, "rate": 50, "payout": 2000}],
        "totals": {"Engineering": {"hours": 40, "payout": 2000}},
    }
    assert json.loads(json_str) == expected


def test_report_to_json_file(tmp_path: Path):
    report_data = {
        "Engineering": [
            {"name": "John Doe", "hours": 40, "rate": 50, "payout": 2000},
        ]
    }
    report = Report(report_data, compute_total_for={"hours", "payout"})
    file_path = tmp_path / "report.json"
    with open(file_path, "w", encoding="UTF-8") as fp:
        report.to_json(fp)
    with open(file_path, "r", encoding="UTF-8") as fp:
        result = json.load(fp)
    expected = {
        "Engineering": [{"name": "John Doe", "hours": 40, "rate": 50, "payout": 2000}],
        "totals": {"Engineering": {"hours": 40, "payout": 2000}},
    }
    assert result == expected


def test_departments_reporter_create_payout_report():
    employees = [
        Employee(
            id=1,
            name="John Doe",
            department="Engineering",
            hours_worked=40,
            hourly_rate=50,
        ),
        Employee(
            id=2,
            name="Jane Smith",
            department="Engineering",
            hours_worked=35,
            hourly_rate=45,
        ),
        Employee(
            id=3,
            name="Bob Johnson",
            department="Marketing",
            hours_worked=30,
            hourly_rate=60,
        ),
    ]
    reporter = DepartmentsReporter(employees)
    report = reporter.create_payout_report()

    assert "Engineering" in report
    assert "Marketing" in report
    assert len(report["Engineering"]) == 2
    assert len(report["Marketing"]) == 1
    assert report["Engineering"][0] == {
        "name": "John Doe",
        "hours": 40,
        "rate": 50,
        "payout": 2000,
    }
    assert report.total_values["Engineering"] == {"hours": 75, "payout": 3575}
    assert report.total_values["Marketing"] == {"hours": 30, "payout": 1800}
