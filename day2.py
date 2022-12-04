from utils import read_input


def part_one():
    point_matrix = {"X": 1, "Y": 2, "Z": 3}
    win_against = {"X": "C", "Y": "A", "Z": "B"}
    draw_against = {"X": "A", "Y": "B", "Z": "C"}
    total_point = 0
    for line in read_input("day2.txt"):
        opponent, me = line.split(" ")
        total_point += point_matrix[me]
        if draw_against[me] == opponent:
            total_point += 3
        elif win_against[me] == opponent:
            total_point += 6
    return total_point


def part_two():
    point_matrix = {"A": 1, "B": 2, "C": 3}
    win_against = {"A": "C", "B": "A", "C": "B"}
    play_to_win = {v: k for k, v in win_against.items()}
    total_point = 0
    for line in read_input("day2.txt"):
        opponent, outcome = line.split(" ")
        match outcome:
            case "X":  # loose
                total_point += point_matrix[win_against[opponent]]
            case "Y":  # draw
                total_point += point_matrix[opponent]
                total_point += 3
            case "Z":  # win
                total_point += point_matrix[play_to_win[opponent]]
                total_point += 6
    return total_point


if __name__ == "__main__":
    print(part_one())
    print(part_two())
