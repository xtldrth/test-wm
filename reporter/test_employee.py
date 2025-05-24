import pytest

from reporter import Employee


def test_employee_from_dict():
    data = {
        "id": "1",
        "name": "John Doe",
        "department": "Engineering",
        "hours_worked": "40",
        "hourly_rate": "50",
    }
    employee = Employee.from_dict(data)
    assert employee.id == 1
    assert employee.name == "John Doe"
    assert employee.department == "Engineering"
    assert employee.hours_worked == 40
    assert employee.hourly_rate == 50


def test_employee_from_dict_with_salary_alias():
    data = {
        "id": "1",
        "name": "John Doe",
        "department": "Engineering",
        "hours_worked": "40",
        "salary": "50",
    }
    employee = Employee.from_dict(data)
    assert employee.hourly_rate == 50


def test_employee_to_dict():
    employee = Employee(
        id=1, name="John Doe", department="Engineering", hours_worked=40, hourly_rate=50
    )
    expected = {
        "id": 1,
        "name": "John Doe",
        "department": "Engineering",
        "hours_worked": 40,
        "hourly_rate": 50,
    }
    assert employee.to_dict() == expected
