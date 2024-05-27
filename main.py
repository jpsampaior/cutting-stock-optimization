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

    operator.set_decision_variables()
    operator.set_constraints()
    operator.set_objective()
    operator.print_optimal_solution()