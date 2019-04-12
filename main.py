import os, sys, numpy, random, copy, solver, re

def wellCond(size):
    return [[10/(1 + 2*abs(i - j)) for j in range(size)] for i in range(size)]

def randomMatr(size):
    return [[100*random.random() for i in range(size)] for j in range(size)]

def badCond(size):
    return [[1/(i+j) for i in range(1, size+1)] for j in range(1, size+1)]

modules = {}

for module in map(lambda x: x[:-3], filter(lambda x: x != 'main.py' and x != 'solver.py' and x[-3:] == '.py', os.listdir())):
    exec('import {}'.format(module))
    modules[module] = filter(lambda x: str(getattr(x, '__class__')) == "<class 'type'>" and issubclass(x, solver.Solver), 
                         map(lambda x: getattr(sys.modules[module], x), 
                         sys.modules[module].__dir__()))


for module in modules:
    print("from module: ", module)
    for solver in modules[module]:
        print("method: ", re.match(r"<class '.*?\.(.*)'>", str(solver))[1])
        for size in range(2, 3):
            print("size: ", size)
            for method in ((wellCond, 'with good cond'), (randomMatr, 'with random cells'), (badCond, 'with bad cond')):
                print("matrix", method[1])
                A = method[0](size)
                b = [i for i in range(size)]
                fun = solver().solve

                print("A: ", A)
                print("b: ", b) 
                print("cond(A)", numpy.linalg.cond(A))
                x = fun(copy.deepcopy(A), copy.deepcopy(b))
                print("x: ", fun(A, b))
                print("error: ", numpy.linalg.norm(b - numpy.dot(A, x)))