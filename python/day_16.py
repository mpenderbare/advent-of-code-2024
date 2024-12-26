from enum import Enum, auto
from pathlib import Path
from typing import TypeAlias
from networkx import Graph, shortest_path, all_shortest_paths, all_simple_paths

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / Path(__file__).name.replace(".py", ".txt")
INPUT_PATH = Path(__file__).parent.parent / "input" / Path(__file__).name.replace(".py", ".txt")

Position: TypeAlias = tuple[float, float]
Map: TypeAlias = dict[Position, str]

EXAMPLE_MAPS: list[list[str]] = [
    [
        "#######",
        "#....E#",
        "#.###.#",
        "#S....#",
        "#######",
    ],
    [
        "#######",
        "#....E#",
        "#.#.#.#",
        "#.....#",
        "#.#.#.#",
        "#S....#",
        "#######",
    ]
]


class Direction(Enum):
    N = auto()
    S = auto()
    W = auto()
    E = auto()


OFFSET_FROM_DIRECTION = {
    Direction.N: (0, -0.25),
    Direction.S: (0, 0.25),
    Direction.W: (-0.25, 0),
    Direction.E: (0.25, 0),
}


def get_map_from_file(sample: bool = False) -> Map:
    input_path = SAMPLE_PATH if sample else INPUT_PATH
    with input_path.open("r") as f:
        return {(x, y): char for y, row in enumerate(f.readlines()) for x, char in enumerate(row.strip())}


def get_simple_map(map_number: int) -> Map:
    example_map = EXAMPLE_MAPS[map_number]
    return {(x, y): char for y, row in enumerate(example_map) for x, char in enumerate(row)}


def get_map_width(map: Map) -> int:
    min_x = min(pos[0] for pos in map.keys())
    max_x = max(pos[0] for pos in map.keys())
    return max_x - min_x + 1

def get_map_height(map: Map) -> int:
    min_y = min(pos[1] for pos in map.keys())
    max_y = max(pos[1] for pos in map.keys())
    return max_y - min_y + 1


def display_map(map: Map) -> None:
    width, height = get_map_width(map), get_map_height(map)
    print("".join([str(i) for i in range(width)]))
    for y in range(height):
        print("".join([map[(x, y)] for x in range(width)] + [f" {y}"]))
    print()


def corner_positions_for_map(map: Map) -> list[Position]:
    corner_positions = []
    for (x, y), char in map.items():
        if char != ".":
            continue
        up = map[(x, y - 1)]
        down = map[(x, y + 1)]
        left = map[(x - 1, y)]
        right = map[(x + 1, y)]
        all_onward_dirs = [adj for adj in [up, down, left, right] if adj == "."]
        match len(all_onward_dirs):
            case 4:
                corner_positions.append((x, y))
            case 3:
                corner_positions.append((x, y))
            case 2:
                if (up == "." and down == ".") or (left == "." and right == "."):
                    continue
                corner_positions.append((x, y))
            case 1:
                corner_positions.append((x, y))
            case _:
                raise RuntimeError(f"Unexpected number ({len(all_onward_dirs)}) of onward paths from node ({x}, {y})")
    return corner_positions


def extract_start_and_end_positions_from_map(map: Map) -> tuple[Position, Position]:
    """Also modifies the map to replace the start and end positions with an empty space ('.')"""
    start_positions = [position for position, char in map.items() if char == "S"]
    end_positions = [position for position, char in map.items() if char == "E"]
    assert len(start_positions) == 1
    assert len(end_positions) == 1
    map[start_positions[0]] = "."
    map[end_positions[0]] = "."
    return start_positions[0], end_positions[0]


def length_for_edge(edge: tuple[Position, Position]) -> int:
    (start_x, start_y), (end_x, end_y) = edge
    return abs(end_x - start_x) + abs(end_y - start_y)


def get_edges_from_corner(map: Map, corner_position: Position, corner_positions: list[Position]) -> list[tuple[Position, Position]]:
    corner_x, corner_y = corner_position
    edges = []
    for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        x, y = corner_x + dx, corner_y + dy
        while map[(x, y)] == ".":
            if (x, y) in corner_positions:
                edges.append(((corner_x, corner_y), (x, y)))
                break
            else:
                x, y = x + dx, y + dy
    return [edge for edge in edges if length_for_edge(edge) > 0]


def get_end_point_for_edge_from_node(edge: tuple[Position, Position], node: Position) -> Position:
    return next(position for position in edge if position != node)


def get_direction_for_edge_from_node(edge: tuple[Position, Position], node: Position) -> Direction:
    node_x, node_y = node
    end_x, end_y = get_end_point_for_edge_from_node(edge, node)
    if end_x > node_x:
        return Direction.E
    if end_x < node_x:
        return Direction.W
    if end_y > node_y:
        return Direction.S
    if end_y < node_y:
        return Direction.N
    raise RuntimeError(f"Could not find direction for node ({node_x}, {node_y}) -> ({end_x}, {end_y})")


def replace_corners_with_subgraph(graph: Graph) -> None:
    result = Graph()
    for node in graph.nodes:
        print(f"{node=}")
        x, y = node
        new_nodes = {direction: (x + dx, y + dy) for direction, (dx, dy) in OFFSET_FROM_DIRECTION.items()}
        print(new_nodes)
        old_edges = graph.edges([node])
        print(f"{old_edges=}")
        new_edges: dict[Direction, tuple[Position, Position]] = {}
        for old_edge in old_edges:
            print(f"{old_edge=}")
            assert node in old_edge
            end_position = get_end_point_for_edge_from_node(old_edge, node)
            direction = get_direction_for_edge_from_node(old_edge, node)
            dx, dy = OFFSET_FROM_DIRECTION[direction]
            new_edges[direction] = ((x + dx, y + dy), end_position)
    # TODO: inter-corner edges are easy - just shave off 0.25 from the ends of all the existing ones
    # TODO: new nodes needs to know how many directions exist from a corner to make the right number of sub-nodes
    # TODO: need some kind of function etc. to generate the intra-corner edges from the number of sub-nodes or directions present



def example(map_number: int) -> None:
    map = get_simple_map(map_number)
    # map = get_map_from_file(sample=False)
    display_map(map)
    start_position, end_position = extract_start_and_end_positions_from_map(map)
    corners = corner_positions_for_map(map)
    edges_for_corner = {corner: get_edges_from_corner(map=map, corner_position=corner, corner_positions=corners) for corner in corners}
    graph = Graph()
    for corner, edges in edges_for_corner.items():
        graph.add_node(corner)
        for edge in edges:
            graph.add_edge(*edge, weight=length_for_edge(edge))
    replace_corners_with_subgraph(graph)
    # print("Shortest path:")
    # print(shortest_path(graph, start_position, end_position))



if __name__ == "__main__":
    example(0)
