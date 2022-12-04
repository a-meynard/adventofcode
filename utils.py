def read_input(filename):
    with open(filename, "r") as day_input:
        return [line.strip() for line in day_input.readlines()]
