from machine import Machine

def read_data(filename):
    data = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            data.append(parts)
    return data


if __name__ == '__main__':
    data = read_data("input.txt")

    operator = Machine(data)
    print(operator.get_cut_patterns())