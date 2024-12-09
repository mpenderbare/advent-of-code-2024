from itertools import product
from pathlib import Path
from operator import add, mul
from typing import Callable, Sequence

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / "day_7.txt"
INPUT_PATH = Path(__file__).parent.parent / "input" / "day_7.txt"


def get_calibrations() -> list[tuple[int, list[int]]]:
    with INPUT_PATH.open("r") as f:
        calibrations = [line.strip().split(":") for line in f.readlines()]
        return [(int(target), [int(x) for x in input.strip().split(" ")]) for target, input in calibrations]


def check_calculation(target: int, inputs: list[int], operators: Sequence[Callable[[int, int], int]]) -> bool:
    current = inputs[0]
    for input, operator in zip(inputs[1:], operators):
        current = operator(current, input)
        if current > target:
            return False
    return current == target


def test_check_calculation() -> None:
    test_cases = [
        (190, [10, 19], [add]),
        (190, [10, 19], [mul]),
        (3267, [81, 40, 27], [add, add]),
        (3267, [81, 40, 27], [mul, add]),
        (3267, [81, 40, 27], [add, mul]),
        (3267, [81, 40, 27], [mul, mul]),
    ]
    for target, inputs, operators in test_cases:
        print(f"{target=}   {inputs=}   {operators=}   {check_calculation(target, inputs, operators)}")


def part_1() -> int:
    calibrations = get_calibrations()
    available_operators = [mul, add]
    possible_calibrations = []
    for target, inputs in calibrations:
        for operators in product(available_operators, repeat=len(inputs) - 1):
            if check_calculation(target, inputs, operators):
                possible_calibrations.append((target, inputs, operators))
                break
    print("Possible calibrations:")
    for target, inputs, operators in possible_calibrations:
        print(f"{target=}   {inputs=}   {operators=}")
    return sum(calibration[0] for calibration in possible_calibrations)


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def test_concat() -> None:
    test_cases = [
        (1, 2, 12),
        (123, 456, 123456),
        (100, 10, 10010),
    ]
    for a, b, expected in test_cases:
        print(f"{a=}   {b=}   {concat(a, b) == expected}")


def part_2() -> int:
    calibrations = get_calibrations()
    available_operators = [mul, add, concat]
    possible_calibrations = []
    for target, inputs in calibrations:
        for operators in product(available_operators, repeat=len(inputs) - 1):
            if check_calculation(target, inputs, operators):
                possible_calibrations.append((target, inputs, operators))
                break
    print("Possible calibrations:")
    for target, inputs, operators in possible_calibrations:
        print(f"{target=}   {inputs=}   {operators=}")
    return sum(calibration[0] for calibration in possible_calibrations)


if __name__ == '__main__':
    print(part_2())
