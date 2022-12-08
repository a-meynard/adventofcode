from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from pathlib import Path


def read_input(filename):
    with open(filename, "r") as day_input:
        return [line.strip() for line in day_input.readlines()]


@dataclass(frozen=True)
class File:
    name: str
    size: int


@dataclass
class Folder:
    name: str
    folders: List[Folder] = field(default_factory=list)
    files: List[File] = field(default_factory=list)

    def add_folder(self, folder: Folder):
        # NOTE: Root folder will have an empty name. Storing the root as a subfolder
        # of an existing folder (what this method do) does not make sense and
        # makes future calculations buggy, by escaping it here we solve the calculations
        # problems to their source.
        if folder.name != "":
            self.folders.append(folder)

    def add_file(self, file: File):
        self.files.append(file)

    def size(self) -> int:
        partial_size = sum([folder.size() for folder in self.folders])
        return partial_size + sum([file.size for file in self.files])


@dataclass
class Terminal:
    filesystem: Dict[str, Folder] = field(default_factory=dict)
    current_path: Path = Path("")

    FILESYSTEM_TOTAL_SIZE: int = 70000000
    REQUIRED_SPACE_FOR_UPGRADE: int = 30000000

    def change_directory(self, new_directory):
        self.current_path /= Path(new_directory)
        self.current_path = self.current_path.resolve()

        if self.current_path not in self.filesystem:
            self.filesystem[self.current_path] = Folder(self.current_path.name)
            self.filesystem[self.current_path.parent].add_folder(
                self.filesystem[self.current_path]
            )

    def current_folder(self) -> Folder:
        return self.filesystem[self.current_path]

    def folders_size(self) -> Dict[Path, int]:
        return {path: folder.size() for path, folder in self.filesystem.items()}

    def filesystem_size(self):
        return self.filesystem[Path("/")].size()

    def folders_under(self, limit_size: int) -> List[Tuple(Path, Folder)]:
        return list(filter(lambda x: x[1] < limit_size, self.folders_size().items()))

    def folders_above(self, limit_size: int) -> List[Tuple(Path, Folder)]:
        return list(filter(lambda x: x[1] > limit_size, self.folders_size().items()))

    def select_folder_to_delete(self):
        space_to_free = (
            self.filesystem_size()
            + self.REQUIRED_SPACE_FOR_UPGRADE
            - self.FILESYSTEM_TOTAL_SIZE
        )
        candidate_paths = list(
            filter(lambda x: x[0] != Path("/"), self.folders_above(space_to_free))
        )
        return sorted(candidate_paths, key=lambda x: x[1])[0]


@dataclass
class Interpreter:
    terminal: Terminal
    COMMAND_LINE_PROMPT: str = "$ "

    def handle(self, line: str):
        if self.is_command(line):
            command = line.replace(self.COMMAND_LINE_PROMPT, "")
            if command.startswith("cd"):
                self.terminal.change_directory(command.replace("cd ", ""))
        else:
            # NOTE: We are in the output of an ls command
            if not line.startswith("dir"):
                file = File(line.split(" ")[1], int(line.split(" ")[0]))
                self.terminal.current_folder().add_file(file)
            else:
                # NOTE: This else statement (dir lines) is not necessary for the exercice
                # but I added it for completeness of the solution. It not necessary because
                # the terminal class already build the useful (the one with a size) view
                # of the filesystem thanks to the cd commands typed in the input
                folder = Folder(line.split(" ")[1])
                self.terminal.current_folder().add_folder(folder)

    def is_command(self, line: str):
        return line.startswith(self.COMMAND_LINE_PROMPT)


terminal = Terminal()
interpreter = Interpreter(terminal)
for line in read_input("day7.txt"):
    interpreter.handle(line)

print("part one:", sum([size for _, size in terminal.folders_under(100000)]))
print("part two:", terminal.select_folder_to_delete())
