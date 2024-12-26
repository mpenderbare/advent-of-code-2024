from pathlib import Path
from functools import lru_cache

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / Path(__file__).name.replace(".py", ".txt")
INPUT_PATH = Path(__file__).parent.parent / "input" / Path(__file__).name.replace(".py", ".txt")


def get_stones(sample: bool = False) -> list[str]:
    input_path = SAMPLE_PATH if sample else INPUT_PATH
    with input_path.open("r") as f:
        return [stone for stone in f.readline().strip().split()]


@lru_cache(maxsize=None)
def process_stone(stone: str, blinks: int) -> int:
    if blinks == 0:
        return 1
    if stone == "0":
        return process_stone("1", blinks=blinks - 1)
    if (length := len(stone)) % 2 == 0:
        return process_stone(str(int(stone[:length//2])), blinks=blinks - 1) + process_stone(str(int(stone[length//2:])), blinks=blinks - 1)
    return process_stone(str(int(stone) * 2024), blinks=blinks - 1)


def part_1(sample: bool = False) -> int:
    stones = get_stones(sample)
    blinks = 25
    return sum(process_stone(stone, blinks=blinks) for stone in stones)


def part_2() -> int:
    stones = get_stones(sample=False)
    blinks = 75
    return sum(process_stone(stone, blinks=blinks) for stone in stones)


if __name__ == "__main__":
    print(part_2())
