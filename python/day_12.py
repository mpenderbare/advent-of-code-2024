from pathlib import Path
from typing import TypeAlias, assert_never

import networkx as nx


SAMPLE_PATH = Path(__file__).parent.parent / "sample" / Path(__file__).name.replace(".py", ".txt")
INPUT_PATH = Path(__file__).parent.parent / "input" / Path(__file__).name.replace(".py", ".txt")

Point: TypeAlias = tuple[int, int]
Map: TypeAlias = dict[Point, str]
Box: TypeAlias = tuple[Point, Point, Point, Point]


def get_map_from_file(sample: bool = False) -> Map:
    input_path = SAMPLE_PATH if sample else INPUT_PATH
    with input_path.open("r") as f:
        return {(x, y): value for y, row in enumerate(f.readlines()) for x, value in enumerate(row.strip())}


def map_graph(map: Map) -> nx.Graph:
    allowed_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    graph = nx.Graph()
    for (x, y), value in map.items():
        graph.add_node((x, y), value=value)
        for (dx, dy) in allowed_directions:
            if (adj_node := (x + dx, y + dy)) in map and map[adj_node] == value:
                graph.add_edge((x, y), adj_node)
    return graph


def part_1(sample: bool = False) -> int:
    map = get_map_from_file(sample)
    graph = map_graph(map)
    subgraphs = (graph.subgraph(component) for component in nx.connected_components(graph))
    total_price = 0
    for subgraph in subgraphs:
        total_nodes = subgraph.number_of_nodes()
        total_edges = subgraph.number_of_edges()
        total_price += 2 * total_nodes * (2 * total_nodes - total_edges)  # faces for each node = 4 - edges, but due to double counting need n * (4n - 2e)
    return total_price


def boxes_for_point(point: Point) -> set[Box]:
    boxes = set()
    x, y = point
    for (dx, dy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        box = (
                (x, y),
                (x + dx, y),
                (x, y + dy),
                (x + dx, y + dy),
            )
        boxes.add(box)
    assert len(boxes) == 4
    return boxes


def corner_boxes_for_nodes(nodes: set[Point]) -> set[Box]:
    corner_boxes = set()
    for node in nodes:
        for box in boxes_for_point(node):
            assert box[0] in nodes
            match len(set(box).intersection(nodes)):
                case 1:
                    corner_boxes.add(box)
                case 2:
                    if box[3] in nodes:
                        corner_boxes.add(box)
                case 3:
                    corner_boxes.add(box)
                case 4:
                    continue
                case _:
                    assert_never("Unreachable")
    return corner_boxes



def part_2(sample: bool = False) -> int:
    map = get_map_from_file(sample)
    graph = map_graph(map)
    subgraphs = list(graph.subgraph(component) for component in nx.connected_components(graph))
    total_price = 0
    for subgraph in subgraphs:
        nodes = set(subgraph.nodes.keys())
        corner_boxes = corner_boxes_for_nodes(nodes)
        unique_corner_boxes = set(tuple(sorted(box)) for box in corner_boxes)
        number_of_double_corners = sum(1 for box in unique_corner_boxes if len(set(box).intersection(nodes)) == 2)
        unique_corners = len(unique_corner_boxes)
        sides = unique_corners + number_of_double_corners
        price = subgraph.number_of_nodes() * sides
        total_price += price
    return total_price


if __name__ == "__main__":
    print(part_2(sample=False))
