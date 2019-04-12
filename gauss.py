import solver, numpy

class Gauss(solver.Solver):

    def lineMul(self, x, m):
        self.b[x] = self.b[x] * m
        for i in range(self.w):
            self.A[x][i] *= m

    def lineSub(self, x, y, m):
        self.b[x] -= m * self.b[y]
        for i in range(self.w):
            self.A[x][i] -= m * self.A[y][i]

    def solve(self, A, b):
        self.A = A
        self.b = b
        self.w = len(A[0])
        self.h = len(A)
        for line in range(self.h):
            m = 1/A[line][line]
            self.lineMul(line, m)
            for line0 in range(line + 1, self.h):
                self.lineSub(line0, line, A[line0][line])
        
        return numpy.linalg.solve(A, b)
