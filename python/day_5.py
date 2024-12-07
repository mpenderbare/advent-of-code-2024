from collections import defaultdict
from functools import cmp_to_key
from pathlib import Path

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / "day_5.txt"
INPUT_PATH = Path(__file__).parent.parent / "input" / "day_5.txt"


def get_rules_and_updates() -> tuple[dict[int, list[int]], list[list[int]]]:
    with INPUT_PATH.open("r") as f:
        all_lines = " ".join([line.strip() for line in f.readlines()]).split()
        rules, updates = defaultdict(list), []
        for line in all_lines:
            if "|" in line:
                x, y = line.split("|")
                rules[int(x)].append(int(y))
            else:
                updates.append([int(x) for x in line.split(",")])
        return rules, updates


def part_1() -> int:
    rules, updates = get_rules_and_updates()

    def comparison_func(A: int, B: int) -> int:
        if A == B:
            return 0
        elif A in rules[B]:
            return 1
        else:
            return -1

    middle_page_sum = 0
    for update in updates:
        sorted_update = sorted(update, key=cmp_to_key(comparison_func))
        if update == sorted_update:
            middle_page_sum += update[(len(update) - 1) // 2]
    return middle_page_sum


def part_2() -> int:
    rules, updates = get_rules_and_updates()

    def comparison_func(A: int, B: int) -> int:
        if A == B:
            return 0
        elif A in rules[B]:
            return 1
        else:
            return -1

    middle_page_sum = 0
    for update in updates:
        sorted_update = sorted(update, key=cmp_to_key(comparison_func))
        if update != sorted_update:
            middle_page_sum += sorted_update[(len(sorted_update) - 1) // 2]
    return middle_page_sum


if __name__ == '__main__':
    print(part_2())
