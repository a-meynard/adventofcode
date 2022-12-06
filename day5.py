from utils import read_input
import re

is_in_part_one = False


class Stack:
    def __init__(self) -> None:
        self._stack = []

    def push(self, elem):
        self._stack.append(elem)

    def push_block(self, block):
        self._stack.extend(block)

    def pop(self):
        return self._stack.pop()

    def pop_block(self, amount):
        block = self._stack[len(self._stack) - amount :]
        del self._stack[len(self._stack) - amount :]
        return block

    def __str__(self):
        return "in -> " + " -> ".join(self._stack)


input = read_input("day5.txt", no_strip=True)

instruction_lines = []
stack_lines = []
instruction_mode = False
for line in input:
    if line == "":
        instruction_mode = True
        continue
    if instruction_mode:
        instruction_lines.append(line)
    else:
        stack_lines.append(line)

# print(instruction_lines)
# print(stack_lines)

headers = list(map(int, filter(None, stack_lines[-1].split(" "))))
amount_of_stacks = headers[-1]

stack_lines.pop()


def normalize_stack_line(stack_line, amount_of_stacks):
    return stack_line + " " * (
        amount_of_stacks * 3 + (amount_of_stacks - 1) - len(stack_line)
    )


def crate_space_generator(stack_line, amount_of_stacks):
    i = 0
    n_stack_line = normalize_stack_line(stack_line, amount_of_stacks)
    while i < len(n_stack_line):
        yield n_stack_line[i : i + 3]
        i += 4


def extract_crate_letter(crate_object: str):
    return crate_object.strip().replace("[", "").replace("]", "")


stacks = [Stack() for i in range(amount_of_stacks)]
for stack_line in stack_lines:
    for index, crate in enumerate(crate_space_generator(stack_line, amount_of_stacks)):
        letter = extract_crate_letter(crate)
        if letter:
            # print("stack number", index + 1, "letter pushed:", letter)
            stacks[index].push(letter)

# HACK: we built the stack by reading line by line from top to bottom, this means
# our stacks are in the wrong order, we will be doing a bit of magic here
for stack in stacks:
    stack._stack.reverse()

# print(list(map(str, stacks)))

for instruction in instruction_lines:
    # search instruction components
    match = re.search(r"move (\d+) from (\d) to (\d)", instruction)
    amount = int(match.groups()[0])
    from_column = int(match.groups()[1])
    to_column = int(match.groups()[2])

    # execute instructions
    if is_in_part_one:
        for i in range(amount):
            stacks[to_column - 1].push(stacks[from_column - 1].pop())
    else:
        stacks[to_column - 1].push_block(stacks[from_column - 1].pop_block(amount))

top_letters = ""
for stack in stacks:
    top_letters += stack.pop()
print(top_letters)
