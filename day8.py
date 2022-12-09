from utils import read_input
from typing import List, Generator
from dataclasses import dataclass, field


def transpose(matrix):
    transposed = []
    for i in range(len(matrix[0])):
        transposed.append([sublist[i] for sublist in matrix])
    return transposed


def is_visible(trees: List[int], selected_tree_index: int, strict=False):
    # print(f"({trees}, {selected_tree_index})", end="")
    if selected_tree_index == 0:
        return True

    for i in range(selected_tree_index):
        if strict:
            if trees[selected_tree_index] <= trees[i]:
                return False
        else:
            if trees[selected_tree_index] < trees[i]:
                return False
    return True


def view_distance(trees: List[int]) -> int:
    if len(trees) == 1:
        return 0

    for tree_index in range(1, len(trees)):
        if is_visible(trees, tree_index):
            return tree_index

    return len(trees) - 1


@dataclass(frozen=True)
class Tree:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x};{self.y})"


@dataclass
class Forest:
    matrix: List[List[int]]
    transposed_matrix: List[List[int]] = field(default_factory=list)

    def __post_init__(self):
        self.transposed_matrix = transpose(self.matrix)

    def is_tree_visible(self, tree: Tree):
        return (
            is_visible(self.matrix[tree.y], tree.x)
            or is_visible(self.transposed_matrix[tree.x], tree.y)
            or is_visible(
                list(reversed(self.matrix[tree.y])),
                len(self.matrix[tree.y]) - tree.x - 1,
            )
            or is_visible(
                list(reversed(self.transposed_matrix[tree.x])),
                len(self.transposed_matrix[tree.x]) - tree.y - 1,
            )
        )

    def calculate_scenic_score(self, tree: Tree):
        return (
            view_distance(self.matrix[tree.y][tree.x :])
            * view_distance(list(reversed(self.matrix[tree.y][: tree.x + 1])))
            * view_distance(self.transposed_matrix[tree.x][tree.y :])
            * view_distance(
                list(reversed(self.transposed_matrix[tree.x][: tree.y + 1]))
            )
        )

    def all_tree_spots(self) -> Generator[Tree, None, None]:
        for x in range(len(self.matrix)):
            for y in range(len(self.transposed_matrix)):
                yield Tree(x, y)

    def count_visible_trees(self) -> int:
        return [
            forest.is_tree_visible(position) for position in forest.all_tree_spots()
        ].count(True)

    def best_scenic_score(self):
        return max(
            [self.calculate_scenic_score(tree) for tree in self.all_tree_spots()]
        )


input = read_input("day8.txt")
forest = Forest([list(map(int, line)) for line in input])
print(forest.count_visible_trees())
print(forest.best_scenic_score())
