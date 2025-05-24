import json
from typing import Any, Iterable, TYPE_CHECKING

from .employee import Employee

if TYPE_CHECKING:
    from _typeshed import SupportsWrite

PADDING_BETWEEN_FIELDS = 4


class Report(dict[str, list[dict[str, Any] | dict[Any, Any]]]):
    def __init__(self, *args, compute_total_for: set[str] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_values = self._compute_total_values(compute_total_for)

    def _get_max_fields_len(self) -> dict[str, int]:
        max_fields_len = dict()
        for department in self.values():
            if isinstance(department, list):
                # computing max fields len
                for employee in department:
                    for field, value in employee.items():
                        max_fields_len[field] = max(
                            max_fields_len.get(field, 0), len(str(value))
                        )
            if isinstance(department, dict):
                for field, value in department.items():
                    max_fields_len[field] = max(
                        max_fields_len.get(field, 0), len(str(value))
                    )

            # getting great length between field name length with other lengths
            fields = department[0].keys() if isinstance(department, list) else department.keys()
            for field_name in fields:
                max_fields_len[field_name] = max(
                    max_fields_len[field_name], len(field_name)
                )

        if self.total_values is None:
            return max_fields_len

        for department, totals_values in self.total_values.items():
            for field_name, value in totals_values.items():
                max_fields_len[field_name] = max(
                    max_fields_len[field_name], len(str(value))
                )
        return max_fields_len

    def _compute_total_values(
        self, compute_total_for: set[str] | None
    ) -> dict[str, dict[str, int | float]] | None:
        if compute_total_for is None:
            return None
        totals = dict()
        for department, employees in self.items():
            department_totals = dict()
            for employee in employees:
                for field in compute_total_for:
                    department_totals[field] = employee.get(
                        field, 0
                    ) + department_totals.get(field, 0)
            totals[department] = department_totals
        return totals

    def __str__(self):
        max_fields_len = self._get_max_fields_len()
        department_placeholder_len = (
            max(len(department) for department in self.keys()) + PADDING_BETWEEN_FIELDS
        )
        fields = list(self.values())[0]
        fields = fields[0].keys() if isinstance(fields, list) else fields.keys()

        add_placeholder_and_space = lambda char: char * department_placeholder_len + " "

        result_string = add_placeholder_and_space(" ")
        for field in fields:
            result_string += f"{field:{max_fields_len[field] + PADDING_BETWEEN_FIELDS}}"
        result_string += "\n"

        for department, values in self.items():
            result_string += f"{department}\n"

            if isinstance(values, list):
                # print fields of employees
                for employee in values:
                    result_string += add_placeholder_and_space("-")
                    for field, value in employee.items():
                        result_string += (
                            f"{str(value):{max_fields_len[field] + PADDING_BETWEEN_FIELDS}}"
                        )
                    result_string += "\n"
            if isinstance(values, dict):
                result_string += add_placeholder_and_space("-")
                for field, value in values.items():
                    result_string += (
                        f"{str(value):{max_fields_len[field] + PADDING_BETWEEN_FIELDS}}"
                    )
                    result_string += "\n"
            if self.total_values is None:
                continue

            # print totals
            result_string += add_placeholder_and_space(" ")
            for field in fields:
                if (
                    total_value := self.total_values[department].get(field)
                ) is not None:
                    value = total_value
                else:
                    value = ""
                result_string += (
                    f"{str(value):{max_fields_len[field] + PADDING_BETWEEN_FIELDS}}"
                )
            result_string += "\n"
        return result_string

    def to_json(self, fp: "SupportsWrite[str] | None" = None) -> str | None:
        """
        :param fp: a file like object which supports ``.write()`` if it's provided
        object will be written directly to the file if it isn't, then the result will be returned as string
        """
        if self.total_values is not None:
            self["totals"] = dict()
            print(self.total_values)
            for department, totals_values in self.total_values.items():
                self["totals"][department] = totals_values
        if fp is not None:
            return json.dump(self, fp)
        return json.dumps(self)


class DepartmentsReporter:
    def __init__(self, employees: Iterable[Employee]):
        self.departments_employees: dict[str, list[Employee]] = dict()
        for employee in employees:
            department = employee.department
            if self.departments_employees.get(department) is None:
                self.departments_employees[department] = []
            self.departments_employees[department].append(employee)

    def create_payout_report(self) -> Report:
        """
        Creates a payout report.
        returns: ``Report``
        """
        report_dict = dict()
        for department, employees in self.departments_employees.items():
            processed_departments_employees = []
            for employee in employees:
                payout = employee.hours_worked * employee.hourly_rate
                processed_departments_employees.append(
                    {
                        "name": employee.name,
                        "hours": employee.hours_worked,
                        "rate": employee.hourly_rate,
                        "payout": payout,
                    }
                )
            report_dict[department] = processed_departments_employees
        return Report(
            report_dict,
            compute_total_for={"hours", "payout"},
        )
