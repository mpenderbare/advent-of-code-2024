from pathlib import Path
import re

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / "day_3.txt"
INPUT_PATH = Path(__file__).parent.parent / "input" / "day_3.txt"


def get_instructions() -> list[str]:
    with INPUT_PATH.open("r") as f:
        data = [line.strip() for line in f.readlines()]
        return data


def part_1() -> int:
    instructions = get_instructions()
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    result = sum(int(x) * int(y) for x, y in re.findall(pattern, "".join(instructions)))
    return result


def split_instruction(instruction: str, enabled: bool) -> list[str]:
    result = instruction.split("don't()", 1) if enabled else instruction.split("do()", 1)
    if len(result) == 2:
        return result
    elif len(result) == 1:
        return [result[0], ""]
    else:
        raise ValueError(f"Invalid split instruction: {instruction} while enabled: {enabled}")


def extract_enabled_instructions(instruction: str) -> str:
    enabled = True
    remaining = instruction
    enabled_instructions = []
    while len(remaining) > 0:
        before, after = split_instruction(remaining, enabled)
        if enabled:
            enabled_instructions.append(before)
        remaining = after
        enabled = not enabled
    return "".join(enabled_instructions)


def part_2() -> int:
    instructions = get_instructions()
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    enabled_instructions = extract_enabled_instructions("".join(instructions))
    result = sum(int(x) * int(y) for x, y in re.findall(pattern, "".join(enabled_instructions)))
    return result


if __name__ == '__main__':
    print(part_2())
