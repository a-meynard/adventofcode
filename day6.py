from utils import read_input

input = read_input("day6.txt")[0]

STARTER_PACKET_SIZE = 14


def find_starter(line):
    for i in range(len(line)):
        found = False
        encoutered_char = set()
        for c in line[i : i + STARTER_PACKET_SIZE]:
            if c in encoutered_char:
                found = True
            encoutered_char.add(c)
        if found:
            continue
        return i + STARTER_PACKET_SIZE


print(find_starter(input))
