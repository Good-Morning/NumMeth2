import solver, numpy

class Gauss(solver.Solver):

    def lineMul(self, x, m):
        self.b[x] *= m
        for i in range(self.w):
            self.A[x][i] *= m

    def lineSub(self, x, y, m):
        self.b[x] -= m * self.b[y]
        for i in range(self.w):
            self.A[x][i] -= m * self.A[y][i]

    def transpose(self, x0, y0, x1, y1):
        for i in range(self.w):
            (self.A[y0][i], self.A[y1][i]) = (self.A[y1][i], self.A[y0][i])
        (self.b[y0], self.b[y1]) = (self.b[y1], self.b[y0])
        for i in range(self.h):
            (self.A[i][x0], self.A[i][x1]) = (self.A[i][x1], self.A[i][x0])

    def select(self, x):
        return (x, x)

    def solve(self, A, b):
        self.A = A
        self.b = b
        self.w = len(A[0])
        self.h = len(A)
        transpositions = []
        for line in range(self.h):
            (temp0, temp1) = self.select(line)
            transpositions.append((temp0, temp1))
            self.transpose(line, line, temp0, temp1)
            m = 1/A[line][line]
            self.lineMul(line, m)
            for line0 in range(line + 1, self.h):
                self.lineSub(line0, line, A[line0][line])
        for line in [self.h-i-1 for i in range(self.h)]:
            for line0 in range(line):
                self.lineSub(line0, line, self.A[line0][line])
        for line in [self.h-i-1 for i in range(self.h)]:
            (temp0, temp1) = transpositions.pop()
            self.transpose(line, line, line, temp0)
        return b


class GaussSelectRow(Gauss):

    def select(self, x):
        maxi = x
        for i in range(x, self.w):
            if abs(self.A[x][i]) > abs(self.A[x][maxi]):
                maxi = i
        return (x, maxi)


class GaussSelectColomn(Gauss):

    def select(self, x):
        maxi = x
        for i in range(x, self.h):
            if abs(self.A[i][x]) > abs(self.A[maxi][x]):
                maxi = i
        return (maxi, x)


class GaussSelectCell(Gauss):

    def select(self, x):
        maxi = x
        maxj = x
        for i in range(x, self.h):
            for j in range(x, self.w):
                if abs(self.A[i][j]) > abs(self.A[maxi][maxj]):
                    maxj = j
                    maxi = i
        return (maxi, maxj) 
