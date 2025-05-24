### requirements:
- python 3.12

#### Как запустить:
   ```shell
   python main.py -r payout data/data1.csv data/data2.csv data/data3.csv -o payout.json -p
   ```

### Для запуска тестов:
1. (опционально) Создать виртуальное окружение и активировать его:
    ```shell
    python -m venv venv && . venv/bin/activate
    ```
2. Установить зависимости:
    ```shell
    python -m pip insatll -r requirements.txt
    ```
3. Запустить тесты:
   ```shell
   pytest 
   ```


## Как создавать новые отчеты
Например, чтобы добавить создание отчета для вычисления средней часовой ставки, нужно сделать следующие шаги:
1. В класс ``reporter.Reporter`` добавить метод ``create_avg_hourly_rate_report``
```python
def create_avg_hourly_rate(self) -> Report:
    report = Report()
    for department, employees in self.departments_employees.items():
        report[department] = {
            "avg r/h": f"{round(sum([employee.hourly_rate for employee in employees]) / len(employees), 2) }"
        }
    return report
```
2. Далее, для того чтобы создать отчет в формате ``json`` ничего менять не нужно, 
для того чтобы вывести отчет в ``stdout`` в данном случае также ничего не нужно менять,
но если нужно будет создать отчет, который не будет соответствовать данному типу:
``dict[str, list[dict[str, Any] | dict[Any, Any]]]``
тогда нужно будет изменить метод ``__str__`` в классе ``reporter.Report``
3. Нужно модифицировать ``main.py``, а именно добавить выбор в ``args_parser.add_argument``
```python
args_parser.add_argument(
   "-r",
   "--report",
   help="report type",
   choices=["payout", "avg_hourly_rate"],
                       ^^^^^^^^^^^^^^^ 
   type=str,
   default=None,
   required=True,
)
```
и создавать отчет в зависимости от типа, который был передан
```python
match args.report:
   case "payout":
      report = reporter.create_payout_report()
   case "avg_hourly_rate":
      report = reporter.create_avg_hourly_rate()
   case _:
      raise ValueError(f"Unknown report type: {args.report}")
```
