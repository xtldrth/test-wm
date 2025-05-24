from argparse import ArgumentParser, BooleanOptionalAction

from csv_ import CSV
from reporter import DepartmentsReporter, Employee


def get_employees_from_csv(csv: CSV):
    rows = csv.get_rows()
    for row in rows:
        yield Employee.from_dict(row)


if __name__ == "__main__":
    args_parser = ArgumentParser(description="Creates reports from csv files report")
    args_parser.add_argument(
        "-r",
        "--report",
        help="report type",
        choices=["payout"],
        type=str,
        default=None,
        required=True,
    )
    args_parser.add_argument(
        "-p",
        "--print",
        default=False,
        action=BooleanOptionalAction,
    )
    args_parser.add_argument("files", nargs="+", help="csv file paths")
    args_parser.add_argument(
        "-o", "--output", help="output file path", default="out.json"
    )
    args = args_parser.parse_args()
    with CSV(*args.files) as csv:
        csv_rows_generator = csv.get_rows()
        reporter = DepartmentsReporter(get_employees_from_csv(csv))
        report = reporter.create_payout_report()
        if args.print:
            print(str(report))
        with open(args.output, "w+") as file:
            report.to_json(file)
