from pathlib import Path

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / "day_1.txt"
INPUT_PATH = Path(__file__).parent.parent / "input" / "day_1.txt"


def part_1() -> int:
    with INPUT_PATH.open("r") as f:
        data = [line.split() for line in f.readlines()]
        left, right = list(zip(*data))

    return sum(abs(int(l) - int(r)) for l, r in zip(sorted(left), sorted(right)))


def part_2() -> int:
    with INPUT_PATH.open("r") as f:
        data = [line.split() for line in f.readlines()]
        left, right = list(zip(*data))
        return sum(int(l) * right.count(l) for l in left)


if __name__ == '__main__':
    print(part_2())
