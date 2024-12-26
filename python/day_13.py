from pathlib import Path
from typing import TypeAlias
import re


SAMPLE_PATH = Path(__file__).parent.parent / "sample" / Path(__file__).name.replace(".py", ".txt")
INPUT_PATH = Path(__file__).parent.parent / "input" / Path(__file__).name.replace(".py", ".txt")


Vector2D: TypeAlias = tuple[int, int]


def get_configurations(sample: bool = False) -> list[tuple[Vector2D, Vector2D, Vector2D]]:
    input_path = SAMPLE_PATH if sample else INPUT_PATH
    machine_regex = re.compile(r"^Button A: X\+(?P<x_a>\d+), Y\+(?P<y_a>\d+)\nButton B: X\+(?P<x_b>\d+), Y\+(?P<y_b>\d+)\nPrize: X=(?P<x_p>\d+), Y=(?P<y_p>\d+)$")
    configurations = []
    with input_path.open("r") as f:
        machines = f.read().split("\n\n")
        for machine in machines:
            match = machine_regex.match(machine)
            configurations.append(((int(match.group("x_a")),int(match.group("y_a"))), (int(match.group("x_b")),int(match.group("y_b"))), (int(match.group("x_p")),int(match.group("y_p"))),))
    return configurations


def _is_valid_solution(a: float, b: float, max_button_presses: int | None = None) -> bool:
    integer_solutions = a.is_integer() and b.is_integer()
    valid_button_presses = True if max_button_presses is None else a <= max_button_presses and b <= max_button_presses
    return integer_solutions and valid_button_presses


def part_1(sample: bool = False, debug: bool = False) -> int:
    configurations = get_configurations(sample=sample)
    tokens = 0
    for ((x_a, y_a), (x_b, y_b), (x_p, y_p)) in configurations:
        if debug:
            print(f"A: {x_a} {y_a}")
            print(f"B: {x_b} {y_b}")
            print(f"P: {x_p} {y_p}")
        a = (y_p * x_b - y_b * x_p) / (y_a * x_b - y_b * x_a)
        b = (x_p - a * x_a) / x_b
        if _is_valid_solution(a=a, b=b, max_button_presses=100):
            tokens += 3 * int(a) + int(b)
        if debug:
            print(f"a = {a}   b = {b}")
            print(f"Exact solution: {a.is_integer() and b.is_integer()}")
            print()
    if debug: print(f"Total tokens: {tokens}")
    return tokens


def part_2(sample: bool = False, debug: bool = False) -> int:
    configurations = get_configurations(sample=sample)
    tokens = 0
    offset = 10000000000000
    for ((x_a, y_a), (x_b, y_b), (x_p, y_p)) in configurations:
        x_p += offset
        y_p += offset
        if debug:
            print(f"A: {x_a} {y_a}")
            print(f"B: {x_b} {y_b}")
            print(f"P: {x_p} {y_p}")
        a = (y_p * x_b - y_b * x_p) / (y_a * x_b - y_b * x_a)
        b = (x_p - a * x_a) / x_b
        if _is_valid_solution(a=a, b=b, max_button_presses=None):
            tokens += 3 * int(a) + int(b)
        if debug:
            print(f"a = {a}   b = {b}")
            print(f"Exact solution: {a.is_integer() and b.is_integer()}")
            print()
    if debug: print(f"Total tokens: {tokens}")
    return tokens


if __name__ == "__main__":
    print(part_2(sample=False, debug=False))
