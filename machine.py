from cut_pattern import CutPattern
from ortools.linear_solver import pywraplp

class Machine:
    def __init__(self, data):
        self.bar = int(data[0][0])
        self.num_of_pieces = int(data[0][1])
        self.pieces_and_qty = []
        self.cut_patterns = []
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.infinity = self.solver.Infinity()
        self.objective = self.solver.Objective()
        self.x = []
        self.current_pattern = []

        for i in range(int(self.num_of_pieces)):
            self.pieces_and_qty.append((int(data[i + 1][0]), int(data[i + 1][1])))

    def generate_cut_patterns(self, index, multiplier):
        if index == self.num_of_pieces:
            total = sum(self.current_pattern)
            waste = self.bar - total
            self.cut_patterns.append(CutPattern(self.current_pattern[:], waste))
            return

        for i in range(self.pieces_and_qty[index][0] * multiplier + 1):
            if sum(self.current_pattern) + i * self.pieces_and_qty[index][0] <= self.bar:
                for j in range(i):
                    self.current_pattern.append(self.pieces_and_qty[index][0])
                self.generate_cut_patterns(index + 1, multiplier)
                for j in range(i):
                    self.current_pattern.pop()

    def get_cut_patterns(self):
        self.cut_patterns = []

        self.generate_cut_patterns(0, 1)

        to_remove = self.filter_cut_patterns()

        for combination in to_remove:
            self.cut_patterns.remove(combination)

        return self.cut_patterns

    def filter_cut_patterns(self):
        min_piece = min(self.pieces_and_qty)[0]

        to_remove = []

        for pattern in self.cut_patterns:
            if pattern.waste >= min_piece:
                to_remove.append(pattern)

        return to_remove

    def set_decision_variables(self):
        for i, pattern in enumerate(self.cut_patterns):
            self.x.append(self.solver.NumVar(0, self.infinity, f'pattern_{i}'))

    def set_constraints(self):
        # Adicionar restrições para garantir que a demanda de cada peça seja atendida
        for piece_index, (piece_length, piece_qty) in enumerate(self.pieces_and_qty):
            constraint = self.solver.RowConstraint(piece_qty, self.infinity, f'piece_{piece_index}_constraint')
            for i, pattern in enumerate(self.cut_patterns):
                if piece_length in pattern.arrayPieces:
                    constraint.SetCoefficient(self.x[i], pattern.arrayPieces.count(piece_length))

    def set_objective(self):
        for i in range(len(self.cut_patterns)):
            self.objective.SetCoefficient(self.x[i], self.cut_patterns[i].waste)

        self.objective.SetMinimization()

    def print_optimal_solution(self):
        if self.solver.Solve() == pywraplp.Solver.OPTIMAL:
            print('Política de corte: \n')
            for i in range(len(self.x)):
                pattern = ' + '.join(map(str, self.cut_patterns[i].arrayPieces))
                print(f'Corte: {pattern}\n'
                      f'Desperdício: {self.cut_patterns[i].waste}\n'
                      f'Quantidade: {int(self.x[i].solution_value())}\n')

            print(f"\nDesperdício total: {int(self.solver.Objective().Value())}")
        else:
            print("Solução ótima não encontrada.")




