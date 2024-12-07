from pathlib import Path

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / "day_4.txt"
INPUT_PATH = Path(__file__).parent.parent / "input" / "day_4.txt"


def get_grid() -> list[str]:
    with INPUT_PATH.open("r") as f:
        grid = [line.strip() for line in f.readlines()]
        return grid


def words_from_position(grid: list[str], position: tuple[int, int], length: int) -> list[str]:
    width = len(grid[0])
    height = len(grid)
    words = []
    x, y = position
    words.append("".join(grid[j][i] for i, j in zip(range(x, min(width, x + length)), range(y, min(height, y + length)))))  # SE
    words.append("".join(grid[y][i] for i in range(x, min(width, x + length))))  # E
    words.append("".join(grid[j][i] for i, j in zip(range(x, min(width, x + length)), range(y, max(-1, y - length), -1))))  # NE
    words.append("".join(grid[j][x] for j in range(y, max(-1, y - length), -1)))  # N
    words.append("".join(grid[j][i] for i, j in zip(range(x, max(-1, x - length), -1), range(y, max(-1, y - length), -1))))  # NW
    words.append("".join(grid[y][i] for i in range(x, max(-1, x - length), -1)))  # W
    words.append("".join(grid[j][i] for i, j in zip(range(x, max(-1, x - length), -1), range(y, min(height, y + length)))))  # SW
    words.append("".join(grid[j][x] for j in range(y, min(height, y + length))))  # S
    return words


def test_words_from_position():
    grid = [
        "abcde",
        "fghij",
        "klmno",
        "pqrst",
        "uvwxy",
    ]
    expected = [
        "msy",
        "mno",
        "mie",
        "mhc",
        "mga",
        "mlk",
        "mqu",
        "mrw",
    ]
    for expected, actual in zip(expected, words_from_position(grid, (4, 4), 4)):
        print(f"{expected == actual}    {expected=}    {actual=}")


def part_1() -> int:
    grid = get_grid()
    width = len(grid[0])
    height = len(grid)
    starting_positions = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "X":
                starting_positions += ((x, y) for word in words_from_position(grid, (x, y), 4) if word == "XMAS")
    return len(starting_positions)


def crossing_words_from_position(grid: list[str], position: tuple[int, int]) -> list[str]:
    x, y = position
    return [
        "".join(grid[y + i][x + i] for i in range(-1, 2)),
        "".join(grid[y - i][x + i] for i in range(-1, 2)),
    ]


def part_2() -> int:
    grid = get_grid()
    width = len(grid[0])
    height = len(grid)
    acceptable_words = ["MAS", "SAM"]
    total = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if grid[y][x] == "A" and all(word in acceptable_words for word in crossing_words_from_position(grid, (x, y))):
                total += 1

    return total


if __name__ == '__main__':
    print(part_2())
