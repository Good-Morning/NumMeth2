import numpy

class Solver:

    def solve(self, A, b):
        return (numpy.linalg.solve(A, b), 1)
