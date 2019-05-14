import random
import numpy as np
import solver

class Jacobi(solver.Solver):

    def D(self, a):
        return np.identity(len(a)) * a.diagonal()

    def invD(self, a):
        return np.linalg.inv(self.D(a))

    def C(self, a):
        return np.dot(self.invD(a), (self.D(a) - a))

    def jacobiG(self, a, b):
        return np.dot(self.invD(a),  b)

    def norm(self, x):
        return np.linalg.norm(x)

    def Jacobi(self, a, b, eps=10**-3, maxIters=10**5):
        c = self.C(a)
        normC = self.norm(c)
        g = self.jacobiG(a, b)
        x = b
        xNew = np.dot(c, x) + g
        itersCount = 0
        while (self.norm(xNew - x) > eps * ((1 - normC) / normC)) and itersCount < maxIters:
            itersCount += 1
            x = xNew
            xNew = np.dot(c, x) + g
        return xNew, itersCount #, np.dot(a, x) - b


    def solve(self, a, b, **kwargs):
        a = np.array(a)
        b = np.array(b)
        return self.Jacobi(a, b, **kwargs)


class Gradients(solver.Solver):

    def gradientsG(self, a, prevX, b):
        return np.dot(a, prevX) - b


    def gradientD(self, g, prevG, prevD):
        numerator = np.dot(g.transpose(), g)
        denominator = np.dot(prevG.transpose(), prevG)
        return (-g + np.dot(numerator / denominator, prevD))


    def gradientS(self, a, d, g):
        numerator = np.dot(d, g)
        denominator = np.dot(np.dot(d.transpose(), a), d)
        return (numerator / denominator)


    def gradients(self, a, b, eps=10**-3, maxIters=10**5):
        x = np.zeros(len(a))
        d = np.zeros(len(a))
        g = -b
        itersCount = 0
        prevX = np.full(len(a), 10**9)
        while np.linalg.norm(prevX - x) > eps and itersCount < maxIters:
            itersCount += 1
            gNew = -self.gradientsG(a, x, b)
            dNew = -self.gradientD(gNew, g, d)
            s = self.gradientS(a, dNew, gNew)
            xNew = x + np.dot(s, dNew)
            prevX = x
            x = xNew
            d = dNew
            g = gNew
        return x, itersCount #, np.dot(a, x) - b


    def solve(self, a, b, **kwargs):
        a = np.array(a)
        b = np.array(b)
        return self.gradients(a, b, **kwargs)
