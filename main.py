from machine import Machine


def read_data(filename):
    data = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            data.append(parts)
    return data


if __name__ == '__main__':
    operator = Machine(read_data("input.txt"))
    cut_patterns = operator.get_cut_patterns()

    for pattern in cut_patterns:
        print(f"Corte: {pattern.arrayPieces}\nDesperdício: {pattern.waste}\n")