from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from time import perf_counter
from typing import TypeAlias
from copy import deepcopy

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / "day_6.txt"
INPUT_PATH = Path(__file__).parent.parent / "input" / "day_6.txt"


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class CellState(Enum):
    UNVISITED = auto()
    VISITED = auto()
    OBSTACLE = auto()


Position: TypeAlias = tuple[int, int]  # (x, y)
Turn: TypeAlias = tuple[Position, Direction]
Map: TypeAlias = list[list[CellState]]


@dataclass
class Guard:
    map: Map
    position: Position
    direction: Direction
    turns: list[Turn]

    @property
    def _height(self) -> int:
        return len(self.map)

    @property
    def _width(self) -> int:
        return len(self.map[0])

    @staticmethod
    def _direction_to_char(direction: Direction) -> str:
        match direction:
            case Direction.UP:
                return "^"
            case Direction.DOWN:
                return "v"
            case Direction.LEFT:
                return "<"
            case Direction.RIGHT:
                return ">"

    def display_current_state(self) -> None:
        display_map = []
        for y, row in enumerate(self.map):
            display_row = []
            for x, cell in enumerate(row):
                if (x, y) == self.position:
                    display_row.append(self._direction_to_char(self.direction))
                else:
                    match cell:
                        case CellState.UNVISITED:
                            display_row.append(".")
                        case CellState.VISITED:
                            display_row.append("X")
                        case CellState.OBSTACLE:
                            display_row.append("#")
            display_map.append("".join(display_row))
        for row in display_map:
            print(row)

    def _turn_right(self) -> None:
        match self.direction:
            case Direction.RIGHT:
                self.direction = Direction.DOWN
            case Direction.DOWN:
                self.direction = Direction.LEFT
            case Direction.LEFT:
                self.direction = Direction.UP
            case Direction.UP:
                self.direction = Direction.RIGHT

    def _next_position(self) -> Position:
        x, y = self.position
        match self.direction:
            case Direction.RIGHT:
                return x + 1, y
            case Direction.LEFT:
                return x - 1, y
            case Direction.DOWN:
                return x, y + 1
            case Direction.UP:
                return x, y - 1

    def _position_inside_map(self, position: Position) -> bool:
        return 0 <= position[0] < self._width and 0 <= position[1] < self._height

    def inside_map(self) -> bool:
        return self._position_inside_map(self.position)

    def step(self) -> None:
        x, y = self.position
        self.map[y][x] = CellState.VISITED
        next_x, next_y = self._next_position()
        if self._position_inside_map((next_x, next_y)) and self.map[next_y][next_x] == CellState.OBSTACLE:
            self._turn_right()
            self.turns.append(((next_x, next_y), self.direction))
        else:
            self.position = next_x, next_y

    @property
    def visited_positions(self) -> list[Position]:
        return [(x, y) for y, row in enumerate(self.map) for x, cell in enumerate(row) if cell == CellState.VISITED]


def get_map_and_start_position() -> tuple[Map, Position]:
    with INPUT_PATH.open("r") as f:
        input_map = [line.strip() for line in f.readlines()]
        map = []
        start_position = None
        for y, input_row in enumerate(input_map):
            row = []
            for x, cell in enumerate(input_row):
                match cell:
                    case ".":
                        row.append(CellState.UNVISITED)
                    case "#":
                        row.append(CellState.OBSTACLE)
                    case "^":
                        row.append(CellState.VISITED)
                        start_position = (x, y)
                    case _:
                        raise ValueError("Invalid cell state")
            map.append(row)
        return map, start_position


def part_1() -> int:
    map, start_position = get_map_and_start_position()
    guard = Guard(map=map, position=start_position, direction=Direction.UP, turns=[])
    while guard.inside_map():
        guard.step()
    return len(guard.visited_positions)


def map_with_obstacle_at_position(map: Map, obstacle_position: Position) -> Map:
    new_map = deepcopy(map)
    new_map[obstacle_position[1]][obstacle_position[0]] = CellState.OBSTACLE
    return new_map


def part_2() -> int:
    map, start_position = get_map_and_start_position()
    guard = Guard(map=map, position=start_position, direction=Direction.UP, turns=[])
    while guard.inside_map():
        guard.step()
    new_obstacle_positions = guard.visited_positions
    new_obstacle_positions.remove(start_position)
    loop_obstacle_positions = []
    for new_obstacle_position in new_obstacle_positions:
        modified_map = map_with_obstacle_at_position(map=map, obstacle_position=new_obstacle_position)
        new_guard = Guard(map=modified_map, position=start_position, direction=Direction.UP, turns=[])
        while new_guard.inside_map():
            new_guard.step()
            if len(new_guard.turns) != len(set(new_guard.turns)):  # need a method to check for loops
                loop_obstacle_positions.append(new_obstacle_position)
                break
    return len(loop_obstacle_positions)


if __name__ == "__main__":
    start = perf_counter()
    result = part_2()
    end = perf_counter()
    print(f"Part 2: {result} in {end - start} seconds")


