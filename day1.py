class PartOne:
    def __init__(self) -> None:
        with open("day1.txt", "r") as day1_input:
            self.input = [line.strip() for line in day1_input.readlines()]

    def find_all_blank_spot(self):
        blank_spots = []
        for index, line in enumerate(self.input):
            if line == "":
                blank_spots.append(index)
        return blank_spots

    def input_for_each_elf(self):
        current_index = 0
        curated_input = list(map(lambda x: int(x) if x else None, self.input))
        for blank_spot in self.find_all_blank_spot():
            yield curated_input[current_index:blank_spot]
            current_index = blank_spot + 1
        yield curated_input[current_index:]

    def sum_calories_for_each_elf(self):
        return [sum(elf) for elf in self.input_for_each_elf()]

    def handle(self):
        return max(self.sum_calories_for_each_elf())


class PartTwo:
    def __init__(self) -> None:
        self.elves = PartOne().sum_calories_for_each_elf()

    def handle(self):
        return sum(sorted(self.elves, reverse=True)[:3])


if __name__ == "__main__":
    print(PartOne().handle())
    print(PartTwo().handle())
