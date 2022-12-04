from utils import read_input


def range_contains(range1, range2):
    return range1.start >= range2.start and range1.stop <= range2.stop


def range_overlap(range1, range2):
    return range1.stop >= range2.start and range1.start <= range2.stop


def is_fully_contained(x, y):
    first, second = range(int(x[0]), int(x[1])), range(int(y[0]), int(y[1]))
    return range_contains(first, second) or range_contains(second, first)


def are_overlap(x, y):
    first, second = range(int(x[0]), int(x[1])), range(int(y[0]), int(y[1]))
    return range_overlap(first, second) or range_overlap(second, first)


input = read_input("day4.txt")
contained = [
    is_fully_contained(*map(lambda x: x.split("-"), line.split(","))) for line in input
]
overlaps = [
    are_overlap(*map(lambda x: x.split("-"), line.split(","))) for line in input
]

print(len(list(filter(None, contained))))
print(len(list(filter(None, overlaps))))
