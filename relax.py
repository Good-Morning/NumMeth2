import numpy, random, math, solver

def transformA(a):
    res = -(a.transpose() / (a.diagonal())).transpose()
    b = numpy.identity(len (res)) * res.diagonal()
    return res - b

def transformB(a, b):
    return b / a.diagonal()

class Relax(solver.Solver):

    def relax(self, c, d, eps, w):
        n = len (d)
        x = numpy.zeros(n)
        # x = numpy.array([0.2, 0.16, 0])
        MAXIT = 100000
        for i in range(MAXIT):
            xnew = x.copy()
            
            
            for i in range (n):
                xnew[i] = numpy.dot (c[i], xnew) + d[i]
                xnew[i] = xnew[i] + (w - 1) * (xnew[i] - x[i])
            if (math.sqrt(sum((xnew - x)**2)) < eps):
                print(i)
                return xnew
            # print(xnew)
            # print(x)
            # print("===")
            x = xnew
        return [math.nan]

    def solve (self, a, b):
        a = numpy.array(a)
        b = numpy.array(b)
        return self.relax(transformA(a), transformB(a, b), 0.001, 1.25)
	

class Seidel(solver.Solver):

    def seidel(self, c, d, eps):
        n = len (d)
        x = numpy.zeros(n)
        # x = numpy.array([0.2, 0.16, 0])
        MAXIT = 100000
        for i in range(MAXIT):
            xnew = x.copy()
            for i in range (n):
                xnew[i] = numpy.dot (c[i], xnew) + d[i]
            if (math.sqrt(sum((xnew - x)**2)) < eps):
                print(i)
                return xnew
            x = xnew
        return [math.nan]
    
    def solve(self, a, b):
        a = numpy.array(a)
        b = numpy.array(b)
        return self.seidel(transformA(a), transformB(a, b), 0.001)