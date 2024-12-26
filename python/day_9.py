from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path

SAMPLE_PATH = Path(__file__).parent.parent / "sample" / Path(__file__).name.replace(".py", ".txt")
INPUT_PATH = Path(__file__).parent.parent / "input" / Path(__file__).name.replace(".py", ".txt")


def get_disk_map(sample: bool = False) -> str:
    input_path = SAMPLE_PATH if sample else INPUT_PATH
    with input_path.open("r") as f:
        return f.readline().strip()


def part_1(sample: bool = False) -> int:
    disk_map = get_disk_map(sample)
    data_blocks =  [int(b) for b in disk_map[::2]]
    empty_blocks = [int(b) for b in disk_map[1::2]]
    moved_data = []
    while len(moved_data) < len(data_blocks):
        moved_block = []
        for _ in range(empty_blocks[0]):
            if len(moved_data) + 1 >= len(data_blocks):
                break
            elif data_blocks[-1] > 1:
                data_blocks[-1] -= 1
                moved_block.append(len(data_blocks) - 1)
            else:
                moved_block.append(len(data_blocks) - 1)
                data_blocks.pop()
        moved_data.append(moved_block)
        empty_blocks.pop(0)

    idx = 0
    total = 0
    for block_idx, (data_block, moved_block) in enumerate(zip_longest(data_blocks, moved_data, fillvalue=[0])):
        for j in range(data_block):
            s = idx * block_idx
            total += s
            idx += 1
        for moved_datum in moved_block:
            s = idx * moved_datum
            total += s
            idx += 1

    return total


@dataclass
class DataBlock:
    start_idx: int
    value: int
    length: int

    def to_string(self) -> str:
        return str(self.value) * self.length


@dataclass
class EmptyBlock:
    start_idx: int
    length: int

    def to_string(self) -> str:
        return "." * self.length


def display_state(data_blocks: list[DataBlock], empty_blocks: list[EmptyBlock]) -> str:
    idx = 0
    display = []
    all_blocks = data_blocks + empty_blocks
    idx_to_block = {block.start_idx: block for block in all_blocks}
    while idx <= max(all_blocks, key=lambda b: b.start_idx).start_idx:
        block = idx_to_block[idx]
        display.append(block.to_string())
        idx += block.length
    return "".join(display)


def checksum(data_blocks: list[DataBlock]) -> int:
    total = 0
    for data_block in data_blocks:
        total += sum(data_block.value * (data_block.start_idx + i) for i in range(data_block.length))
    return total


def part_2(sample: bool = False) -> int:
    disk_map = get_disk_map(sample)
    encoded_data_blocks =  [int(b) for b in disk_map[::2]]
    assert all(x > 0 for x in encoded_data_blocks)
    encoded_empty_blocks = [int(b) for b in disk_map[1::2]]
    data_blocks = []
    empty_blocks = []
    idx = 0
    for i, (data_block, empty_block) in enumerate(zip_longest(encoded_data_blocks, encoded_empty_blocks)):
        if data_block:
            data_blocks.append(
                DataBlock(
                    start_idx=idx,
                    value=i,
                    length=data_block,
                )
            )
            idx += data_block
        if empty_block:
            empty_blocks.append(
                EmptyBlock(
                    start_idx=idx,
                    length=empty_block,
                )
            )
            idx += empty_block

    for data_block in reversed(data_blocks):
        for empty_block in empty_blocks:
            if empty_block.start_idx > data_block.start_idx:
                break
            if data_block.length <= empty_block.length:
                data_block.start_idx = empty_block.start_idx
                empty_block.start_idx += data_block.length
                empty_block.length -= data_block.length
                if empty_block.length == 0:
                    empty_blocks.remove(empty_block)
                break
    return checksum(data_blocks)


if __name__ == "__main__":
    print(part_2(sample=False))
