def read_input(filename, no_strip=False):
    with open(filename, "r") as day_input:
        if no_strip:
            return [line.replace("\n", "") for line in day_input.readlines()]
        else:
            return [line.strip() for line in day_input.readlines()]
