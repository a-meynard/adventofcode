from utils import read_input
from dataclasses import dataclass, field
from typing import Dict, List, Callable
from itertools import count


@dataclass
class Registers:
    main: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        self.main = {"X": 1}


@dataclass
class Operation:
    name: str
    cost: int
    operands: List[str] = field(default_factory=list)

    def handle(self, registers: Registers, operands: List[str]):
        match self.name:
            case "addx":
                registers.main["X"] += int(operands[0])


@dataclass
class CPU:
    registers: Registers = field(default_factory=Registers)
    tick: int = 0
    operations: List[Operation] = field(default_factory=list)

    def add_operation(self, operation: Operation):
        self.operations.append(operation)

    def cycle(self):
        for operation in self.operations:
            # print(operation.name)
            for i in range(operation.cost):
                self.tick += 1
                yield
            operation.handle(self.registers, operation.operands)
        yield


SCREEN_SIZE_NB_LINES = 6
SCREEN_SIZE_NB_COLUMN = 40


@dataclass(frozen=True)
class Cursor:
    x: int
    y: int


@dataclass
class CRT:
    drawing: List[str] = field(default_factory=list)

    def cycle(
        self,
        cpu_register: Registers,
        condition_function: Callable[[Registers, Cursor], bool],
    ):
        for i in range(SCREEN_SIZE_NB_LINES):
            line = ""
            for j in range(SCREEN_SIZE_NB_COLUMN):
                if condition_function(cpu_register, Cursor(j, i)):
                    line += "#"
                else:
                    line += "."
                    print(i, j)
                yield
            self.drawing.append(line)
        yield

    def draw(self):
        for line in self.drawing:
            print(line)


def is_register_on_position(registers: Registers, cursor: Cursor) -> bool:
    return registers.main["X"] - 1 <= cursor.x <= registers.main["X"] + 1


cpu = CPU()
cost_map = {"addx": 2, "noop": 1}
for line in read_input("day10.txt"):
    op_name = line.split(" ")[0]
    cpu.add_operation(Operation(op_name, cost_map[op_name], line.split(" ")[1:]))

crt = CRT()

probe_gen = count(20, 40)
probe = next(probe_gen)
total = 0
for ccpu, ccrt in zip(cpu.cycle(), crt.cycle(cpu.registers, is_register_on_position)):
    if cpu.tick == probe:
        total += cpu.tick * cpu.registers.main["X"]
        probe = next(probe_gen)

print(total)
crt.draw()
