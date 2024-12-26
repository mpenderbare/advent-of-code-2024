from operator import itemgetter
from pathlib import Path
from typing import TypeAlias

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / Path(__file__).name.replace(".py", ".txt")
INPUT_PATH = Path(__file__).parent.parent / "input" / Path(__file__).name.replace(".py", ".txt")


Map: TypeAlias = list[list[str]]
Point: TypeAlias = tuple[int, int]

DIRECTION_FROM_MOVE: dict[str, Point] = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def get_map_and_moves_from_simple_example(part_2: bool = False) -> tuple[Map, str]:
    map_lines = [
        "##############",
        "##......##..##",
        "##..........##",
        "##....[][]@.##",
        "##....[]....##",
        "##..........##",
        "##############",
    ] if part_2 else [
        "########",
        "#..O.O.#",
        "##@.O..#",
        "#...O..#",
        "#.#.O..#",
        "#...O..#",
        "#......#",
        "########",
    ]
    moves = "<vv<<^^<<^^" if part_2 else "<^^>>>vv<v>>v<<"
    return [[str(x) for x in line] for line in map_lines], moves


def convert_map_string_for_part_2(map_str: str) -> str:
    return map_str.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")


def get_map_and_moves_from_file(sample: bool = False, part_2: bool = False) -> tuple[Map, str]:
    input_path = SAMPLE_PATH if sample else INPUT_PATH
    with input_path.open("r") as f:
        map_string, moves_string = f.read().split("\n\n")
        map_string = convert_map_string_for_part_2(map_string) if part_2 else map_string
        return [[str(x) for x in line] for line in map_string.split("\n")], moves_string.replace("\n", "")


def get_robot_position(map: Map) -> Point:
    for y, row in enumerate(map):
        for x, char in enumerate(row):
            if char == "@": return x, y


def display_map(map: Map) -> None:
    for row in map:
        print("".join(row))
    print()


def sum_of_box_gps_coords(map: Map, part_2: bool = False) -> int:
    box_edge = "[" if part_2 else "O"
    total = 0
    for y, row in enumerate(map):
        for x, obj in enumerate(row):
            if obj == box_edge:
                total += 100 * y + x
    return total


def try_move_part_1(map: Map, position: Point, move: str) -> bool:
    x, y = position
    obj = map[y][x]
    if obj == "#":  # wall
        return False
    elif obj == ".":  # empty
        return True
    else:  # robot @ or box O
        dx, dy = DIRECTION_FROM_MOVE[move]
        if success := try_move_part_1(map=map, position=(x + dx, y + dy), move=move):
            map[y + dy][x + dx] = obj
            map[y][x] = "."
        return success


def part_1(sample: bool = False) -> int:
    map, moves = get_map_and_moves_from_file(sample)
    robot_position = get_robot_position(map)
    for move in moves:
        if try_move_part_1(map=map, position=robot_position, move=move):
            x, y = robot_position
            dx, dy = DIRECTION_FROM_MOVE[move]
            robot_position = x + dx, y + dy
    return sum_of_box_gps_coords(map=map)


def try_horizontal_move_part_2(map: Map, position: Point, move: str) -> bool:
    assert move in ["<", ">"]
    x, y = position
    obj = map[y][x]
    if obj == "#":  # wall
        return False
    elif obj == ".":  # empty
        return True
    else:  # robot @ or box O
        dx, dy = DIRECTION_FROM_MOVE[move]
        if success := try_horizontal_move_part_2(map=map, position=(x + dx, y + dy), move=move):
            map[y + dy][x + dx] = obj
            map[y][x] = "."
        return success


def try_vertical_move_part_2(map: Map, position: Point, move: str) -> tuple[bool, list[Point]]:
    assert move in ["^", "v"]
    x, y = position
    obj = map[y][x]
    dx, dy = DIRECTION_FROM_MOVE[move]
    next_obj = map[y + dy][x + dx]
    if next_obj == "#":  # wall
        return False, []
    elif next_obj == ".":  # empty
        return True, []
    elif next_obj == "[":
        l_bracket_success, l_bracket_positions = try_vertical_move_part_2(map=map, position=(x + dx, y + dy), move=move)
        r_bracket_success, r_bracket_positions = try_vertical_move_part_2(map=map, position=(x + dx + 1, y + dy), move=move)
        success = l_bracket_success and r_bracket_success
        return success, [(x + dx, y + dy), (x + dx + 1, y + dy)] + l_bracket_positions + r_bracket_positions
    elif next_obj == "]":
        l_bracket_success, l_bracket_positions = try_vertical_move_part_2(map=map, position=(x + dx - 1, y + dy), move=move)
        r_bracket_success, r_bracket_positions = try_vertical_move_part_2(map=map, position=(x + dx, y + dy), move=move)
        success = l_bracket_success and r_bracket_success
        return success, [(x + dx, y + dy), (x + dx - 1, y + dy)] + l_bracket_positions + r_bracket_positions
    else:
        raise RuntimeError(f"Unknown object: {obj}")


def move_positions(map: Map, positions: list[Point], move: str) -> None:
    assert move in ["^", "v"]
    dx, dy = DIRECTION_FROM_MOVE[move]
    sorted_positions = sorted(positions, key=itemgetter(1), reverse=(move == "v"))
    for x, y in sorted_positions:
        obj = map[y][x]
        map[y + dy][x + dx] = obj
        map[y][x] = "."


def part_2(sample: bool = False) -> int:
    map, moves = get_map_and_moves_from_file(sample, part_2=True)
    robot_position = get_robot_position(map)
    for move in moves:
        if move in ["<", ">"]:
            if try_horizontal_move_part_2(map=map, position=robot_position, move=move):
                x, y = robot_position
                dx, dy = DIRECTION_FROM_MOVE[move]
                robot_position = x + dx, y + dy
        elif move in ["^", "v"]:
            success, boxes_to_move = try_vertical_move_part_2(map=map, position=robot_position, move=move)
            if success:
                positions_to_move = list(set([robot_position] + boxes_to_move))
                move_positions(map=map, positions=positions_to_move, move=move)
                x, y = robot_position
                dx, dy = DIRECTION_FROM_MOVE[move]
                robot_position = x + dx, y + dy
        else:
            raise RuntimeError(f"Unknown move: {move}")
    return sum_of_box_gps_coords(map=map, part_2=True)


if __name__ == "__main__":
    print(part_2(sample=False))
