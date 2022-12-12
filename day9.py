from __future__ import annotations

from dataclasses import dataclass, field, astuple
from utils import read_input
from typing import Tuple, Set
import math


@dataclass(frozen=True, eq=True)
class Position:
    x: int
    y: int

    def move(self, direction: str):
        match direction:
            case "R":
                return Position(self.x + 1, self.y)
            case "U":
                return Position(self.x, self.y + 1)
            case "L":
                return Position(self.x - 1, self.y)
            case "D":
                return Position(self.x, self.y - 1)

    def distance(self, pos: Position) -> int:
        return math.dist(astuple(self), astuple(pos))

    def is_next_to(self, pos: Position):
        print(pos, self)
        return math.floor(self.distance(pos)) <= 1


@dataclass
class Head:
    pos: Position

    def move(self, direction):
        self.pos = self.pos.move(direction)


@dataclass
class Tail:
    pos: Position
    visited_positions: Set[Position] = field(default_factory=set)

    def should_move_in_diagonal(self, head: Head) -> bool:
        return self.pos.y != head.pos.y and self.pos.x != head.pos.x

    def is_too_close_to_head(self, head: Head):
        return self.pos.is_next_to(head.pos)

    def move_to_head(self, head: Head):
        # print("head", head.pos)
        self.visited_positions.add(self.pos)
        if not self.is_too_close_to_head(head):
            # print("both", self.pos, head.pos)
            if tail.should_move_in_diagonal(head):
                # print("moving in diagonale")
                directions = self.determine_diagonale_direction(head)
                self.pos = self.pos.move(directions[0])
                self.pos = self.pos.move(directions[1])
            else:
                # print("moving normally")
                self.pos = self.pos.move(tail.determine_direction(head))

    def determine_direction(self, head: Head) -> str:
        if self.pos.y == head.pos.y:
            if self.pos.x > head.pos.x:
                return "L"
            else:
                return "R"
        elif self.pos.x == head.pos.x:
            if self.pos.y > head.pos.y:
                return "D"
            else:
                return "U"

    def determine_diagonale_direction(self, head: Head) -> Tuple[str, str]:
        if not self.should_move_in_diagonal(head):
            raise ValueError(
                "Asked for diagnoale move but tail is not diagonale from head"
            )

        directions = ["", ""]
        if self.pos.x > head.pos.x:
            directions[0] = "L"
        else:
            directions[0] = "R"

        if self.pos.y > head.pos.y:
            directions[1] = "D"
        else:
            directions[1] = "U"

        return tuple(directions)


head = Head(Position(1000, 1000))
tail = Tail(Position(1000, 1000))

input = read_input("day9.txt")
for line in input:
    # print(line)
    direction, amount_of_steps = line.split(" ")
    for i in range(int(amount_of_steps)):
        # print("round", i)
        head.move(direction)
        tail.move_to_head(head)

print(len(tail.visited_positions))
