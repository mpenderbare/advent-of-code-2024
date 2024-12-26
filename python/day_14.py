import math
from collections import Counter
from enum import StrEnum, auto
from pathlib import Path
from typing import TypeAlias, Optional
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt


SAMPLE_PATH = Path(__file__).parent.parent / "sample" / Path(__file__).name.replace(".py", ".txt")
INPUT_PATH = Path(__file__).parent.parent / "input" / Path(__file__).name.replace(".py", ".txt")

Vector2D: TypeAlias = tuple[int, int]


class Quadrant(StrEnum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()


def get_robots(sample: bool = False) -> list[tuple[[Vector2D, Vector2D]]]:
    input_path = SAMPLE_PATH if sample else INPUT_PATH
    robots = []
    with input_path.open("r") as f:
        regex = re.compile(r"^p=(?P<p_x>-?\d+),(?P<p_y>-?\d+) v=(?P<v_x>-?\d+),(?P<v_y>-?\d+)$")
        for line in f.readlines():
            match = regex.match(line.strip())
            assert match is not None
            robots.append(((int(match.group("p_x")), int(match.group("p_y"))), (int(match.group("v_x")), int(match.group("v_y")))))
    return robots


def position_to_quadrant(position: Vector2D, height: int, width: int) -> Optional[Quadrant]:
    x, y = position
    assert 0 <= x < width
    assert 0 <= y < height
    centre_x = (width - 1) / 2
    centre_y = (height - 1) / 2
    if x < centre_x:
        if y < centre_y:
            return Quadrant.TOP_LEFT
        elif y > centre_y:
            return Quadrant.BOTTOM_LEFT
    elif x > centre_x:
        if y < centre_y:
            return Quadrant.TOP_RIGHT
        elif y > centre_y:
            return Quadrant.BOTTOM_RIGHT
    return None


def part_1(sample: bool = False) -> int:
    robots = get_robots(sample)
    width = 11 if sample else 101
    height = 7 if sample else 103
    time_steps = 100
    final_positions: list[Vector2D] = []
    for robot in robots:
        p_x, p_y = robot[0]
        v_x, v_y = robot[1]
        final_positions.append(((p_x + v_x * time_steps) % width, (p_y + v_y * time_steps) % height))
    counter = Counter(position_to_quadrant(position=position, height=height, width=width) for position in final_positions)
    display_floorplan(robot_positions=final_positions, width=width, height=height)
    return math.prod(count for quadrant, count in counter.items() if quadrant is not None)


def display_floorplan(robot_positions: list[Vector2D], width: int, height: int) -> None:
    counter = Counter(robot_positions)
    floorplan = []
    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) in counter:
                row.append(str(counter[(x, y)]))
            else:
                row.append(".")
        floorplan.append("".join(row))
    for row in floorplan:
        print(row)


def array_from_positions(positions: set[Vector2D], width: int, height: int) -> np.ndarray:
    return np.array([[255 if (x, y) in positions else 0 for x in range(width)] for y in range(height)], dtype=np.uint8)


def part_2(sample: bool = False) -> None:
    robots = get_robots(sample)
    width = 11 if sample else 101
    height = 7 if sample else 103
    min_contour_length = 20
    time_step = 0
    while True:
        robot_positions = {((p_x + v_x * time_step) % width, (p_y + v_y * time_step) % height) for (p_x, p_y), (v_x, v_y) in robots}
        arr = array_from_positions(robot_positions, width, height)
        contours, _ = cv2.findContours(arr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours = [contour for contour in contours if cv2.arcLength(contour, True) > min_contour_length]
        if filtered_contours:
            canvas = np.zeros_like(arr)
            cv2.drawContours(canvas, filtered_contours, -1, 255, 1)
            plt.figure(figsize=(6, 6))
            plt.imshow(canvas, cmap='gray')
            plt.title(f"Time step: {time_step}")
            plt.axis('off')
            plt.show()
        if time_step == 6577:
            display_floorplan(robot_positions=list(robot_positions), width=width, height=height)
        time_step += 1


if __name__ == "__main__":
    print(part_2(sample=False))
    #  time step = 6577
