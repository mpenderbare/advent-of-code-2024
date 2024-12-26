from pathlib import Path
from typing import TypeAlias

import networkx as nx


SAMPLE_PATH = Path(__file__).parent.parent / "sample" / Path(__file__).name.replace(".py", ".txt")
INPUT_PATH = Path(__file__).parent.parent / "input" / Path(__file__).name.replace(".py", ".txt")


Map: TypeAlias = dict[tuple[int, int], int]

def get_map(sample: bool = False) -> Map:
    input_path = SAMPLE_PATH if sample else INPUT_PATH
    with input_path.open("r") as f:
        return {(x, y): int(value) for y, row in enumerate(f.readlines()) for x, value in enumerate(row.strip())}


def map_to_trail_graph(map: Map) -> nx.DiGraph:
    allowed_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    graph = nx.DiGraph()
    for (x, y), value in map.items():
        graph.add_node((x, y), value=value)
        for (dx, dy) in allowed_directions:
            if (adj_node := (x + dx, y + dy)) in map and map[adj_node] == value + 1:
                graph.add_edge((x, y), adj_node)
    return graph


def part_1(sample: bool = False) -> int:
    map = get_map(sample)
    graph = map_to_trail_graph(map)
    start_nodes = [node for node in graph.nodes if graph.nodes[node]["value"] == 0]
    end_nodes = [node for node in graph.nodes if graph.nodes[node]["value"] == 9]
    total = 0
    for start_node in start_nodes:
        total += sum(1 for end_node in end_nodes if len(list(nx.all_simple_paths(graph, start_node, end_node))) > 0)
    return total


def part_2(sample: bool = False) -> int:
    map = get_map(sample)
    graph = map_to_trail_graph(map)
    start_nodes = [node for node in graph.nodes if graph.nodes[node]["value"] == 0]
    end_nodes = [node for node in graph.nodes if graph.nodes[node]["value"] == 9]
    total = 0
    for start_node in start_nodes:
        total += sum(len(list(nx.all_simple_paths(graph, start_node, end_node))) for end_node in end_nodes)
    return total


if __name__ == "__main__":
    print(part_2(sample=False))
