from dataclasses import dataclass
from typing import Any

FIELD_ALIASES = {
    "rate": "hourly_rate",
    "salary": "hourly_rate",
}


@dataclass
class Employee:
    id: int
    name: str
    department: str
    hours_worked: int
    hourly_rate: int

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Employee":
        normalized_dict = {}
        for key, value in d.items():
            if (alias := FIELD_ALIASES.get(key)) is not None:
                normalized_dict[alias] = value
            else:
                normalized_dict[key] = value
        return Employee(
            id=int(normalized_dict.get("id", 0)),
            name=normalized_dict.get("name", ""),
            department=normalized_dict.get("department", ""),
            hours_worked=int(normalized_dict.get("hours_worked", 0)),
            hourly_rate=int(normalized_dict.get("hourly_rate", 0)),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "hours_worked": self.hours_worked,
            "hourly_rate": self.hourly_rate,
        }
