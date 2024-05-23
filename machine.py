class Machine:
    def __init__(self, data):
        self.bar = int(data[0][0])
        self.num_of_pieces = int(data[0][1])
        self.pieces_and_qty = []
        self.cut_patterns = []

        for i in range(int(self.num_of_pieces)):
            self.pieces_and_qty.append((int(data[i + 1][0]), int(data[i + 1][1])))

    def get_cut_patterns(self):
        self.cut_patterns = []
        current_pattern = []

        def generate_cut_patterns(index, multiplier):
            if index == self.num_of_pieces:
                self.cut_patterns.append(current_pattern[:])
                return
            for i in range(self.pieces_and_qty[index][0] * multiplier + 1):
                if sum(current_pattern) + i * self.pieces_and_qty[index][0] <= self.bar:
                    for j in range(i):
                        current_pattern.append(self.pieces_and_qty[index][0])
                    generate_cut_patterns(index + 1, multiplier)
                    for j in range(i):
                        current_pattern.pop()

        generate_cut_patterns(0, 1)
        return self.cut_patterns
