from utils import read_input


def priority(letter):
    if ord("A") <= ord(letter) <= ord("Z"):
        return 27 + ord(letter) - ord("A")
    else:
        return 1 + ord(letter) - ord("a")


def priority_generator(input):
    for line in input:
        first_compartiment = set(line[: int(len(line) / 2)])
        second_compartiment = set(line[int(len(line) / 2) :])
        odd_letter = "".join(first_compartiment.intersection(second_compartiment))
        yield priority(odd_letter)


def get_group_item_type(input):
    for first, second, third in zip(input[::3], input[1::3], input[2::3]):
        yield priority(
            "".join(set(first).intersection(set(second)).intersection(set(third)))
        )


input = read_input("day3.txt")
print(sum(priority_generator(input)))
print(sum(get_group_item_type(input)))
