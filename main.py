import os, sys, numpy, random, copy, solver, re

def goodCond(size):
    return [[10/(1 + 2*abs(i - j)) for j in range(size)] for i in range(size)]

def randCond(size):
    return [[100*random.random() for i in range(size)] for j in range(size)]

def gilbCond(size):
    return [[1/(2+i+j) for i in range(size)] for j in range(size)]

modules = {}

for module in map(lambda x: x[:-3], filter(lambda x: x != 'main.py' and x[-3:] == '.py', os.listdir())):
    exec('import {}'.format(module))
    mod = sys.modules[module]
    modules[module] = [x for x in [getattr(mod, x) for x in dir(mod)] if str(type(x)) == "<class 'type'>" and issubclass(x, solver.Solver)]
modules = {i:modules[i] for i in modules if len(modules[i])}

sizeFrom = 2
sizeTo = 10

tests = [
    ('random   ', [randCond(i) for i in range(sizeFrom, sizeTo+1)]), 
    ('good cond', [goodCond(i) for i in range(sizeFrom, sizeTo+1)]), 
    ('bad cond ', [gilbCond(i) for i in range(sizeFrom, sizeTo+1)]), 
]

with open('output.md', 'w') as output:
    output.write('|module|solver')
    for test in tests:
        output.write('|' + test[0] + '|'.join(map(lambda x: '', range(sizeFrom, sizeTo+1))))
    output.write('|\n|-|-|-'+'|-'.join(map(lambda x: '', range(sizeFrom, len(tests)*sizeTo+1)))+'|\n|||')
    for test in tests:
        output.write('|'.join(map(str, range(sizeFrom, sizeTo+1))) + '|')
    output.write('\n|cond||')
    for testPack in tests:
        for test in testPack[1]:
            output.write('{0:.6g}'.format(numpy.linalg.cond(test)) + '|')
    output.write('\n||\n')
    for module in modules:
        output.write(module + '|')
        flag = False
        for worker in modules[module]:
            if flag:
                output.write('||')
            output.write(re.match(r"<class '.*?\.(.*)'>", str(worker))[1] + '|')
            flag = True
            for testPack in tests:
                for A in testPack[1]:
                    b = [i for i in range(len(A))]
                    fun = worker().solve

                    # print("A: ", A)
                    # print("b: ", b) 
                    # print("cond(A)", numpy.linalg.cond(A))
                    x = fun(copy.deepcopy(A), copy.deepcopy(b))
                    # print("x: ", fun(A, b))
                    output.write('{0:.4g}'.format(numpy.linalg.norm(b - numpy.dot(A, x))) + '|')
            output.write('\n')
                    