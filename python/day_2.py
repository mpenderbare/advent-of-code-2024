from itertools import pairwise, combinations
from pathlib import Path

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / "day_2.txt"
INPUT_PATH = Path(__file__).parent.parent / "input" / "day_2.txt"


def get_reports() -> list[list[int]]:
    with INPUT_PATH.open("r") as f:
        return [[int(x) for x in line.split()] for line in f.readlines()]


def report_is_safe(report: list[int]) -> bool:
    increasing = report == sorted(report)
    decreasing = report == sorted(report, reverse=True)
    levels_close = all(0 < abs(x - y) < 4 for x, y in pairwise(report))
    return levels_close and (increasing or decreasing)


def part_1() -> int:
    reports = get_reports()
    return sum(1 for report in reports if report_is_safe(report))


def exists_safe_altered_report(report: list[int]) -> bool:
    for altered_report in combinations(report, len(report) - 1):
        if report_is_safe(list(altered_report)):
            return True
    return False


def part_2() -> int:
    reports = get_reports()
    safe_reports = 0
    for report in reports:
        if report_is_safe(report):
            safe_reports += 1
        elif exists_safe_altered_report(report):
            safe_reports += 1
    return safe_reports


if __name__ == '__main__':
    print(part_2())
