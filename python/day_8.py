from itertools import permutations
from pathlib import Path
from typing import TypeAlias, Mapping
from collections import defaultdict

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / "day_8.txt"
INPUT_PATH = Path(__file__).parent.parent / "input" / "day_8.txt"


Map: TypeAlias = list[str]
Position: TypeAlias = tuple[int, int]


def get_map(sample: bool = False) -> Map:
    input_path = SAMPLE_PATH if sample else INPUT_PATH
    with input_path.open("r") as f:
        return [line.strip() for line in f.readlines()]


def antenna_positions_from_map(map: Map) -> Mapping[str, list[Position]]:
    antenna_positions = defaultdict(list[Position])
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell != ".":
                antenna_positions[cell].append((x, y))
    return dict(antenna_positions)


def part_1(sample: bool = False) -> int:
    map = get_map(sample=sample)
    height = len(map)
    width = len(map[0])
    antinode_positions = set()
    antenna_positions = antenna_positions_from_map(map)
    for _, positions in antenna_positions.items():
        for pos_a, pos_b in permutations(positions, 2):
            antinode_positions.add(
                (pos_b[0] + (pos_b[0] - pos_a[0]), pos_b[1] + (pos_b[1] - pos_a[1]))
            )
    return len({pos for pos in antinode_positions if 0 <= pos[0] < width and 0 <= pos[1] < height})


def antinode_positions_for_antennae(antenna_a_pos: Position, antenna_b_pos: Position, height: int, width: int) -> set[Position]:
    antinode_positions = set()
    diff: tuple[int, int] = (antenna_b_pos[0] - antenna_a_pos[0], antenna_b_pos[1] - antenna_a_pos[1])
    current = antenna_b_pos
    while 0 <= current[0] < width and 0 <= current[1] < height:
        antinode_positions.add(current)
        current = (current[0] + diff[0], current[1] + diff[1])
    return antinode_positions


def part_2(sample: bool = False) -> int:
    map = get_map(sample=sample)
    height = len(map)
    width = len(map[0])
    antinode_positions = set()
    antenna_positions = antenna_positions_from_map(map)
    for _, positions in antenna_positions.items():
        for pos_a, pos_b in permutations(positions, 2):
            antinode_positions.update(antinode_positions_for_antennae(pos_a, pos_b, height, width))
    return len(antinode_positions)


if __name__ == "__main__":
    print(part_2(sample=False))
