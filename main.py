import os, sys, numpy, random, copy, solver, re
import openpyxl, itertools

def goodCond(size):
    return [[10/(1 + 4*abs(i - j)) for j in range(size)] for i in range(size)]

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

sizeFrom = 5
sizeTo = 6

tests = [
    ('random   ', [randCond(i) for i in range(sizeFrom, sizeTo+1)]), 
    ('good cond', [goodCond(i) for i in range(sizeFrom, sizeTo+1)]), 
    ('bad cond ', [gilbCond(i) for i in range(sizeFrom, sizeTo+1)]), 
]

wb = openpyxl.Workbook()
ws = wb['Sheet']

sizeSize = sizeTo - sizeFrom + 1
ws['A1'] = 'module'
ws['B1'] = 'solver'
ws['A2'] = 'size'
ws['A3'] = 'cond'
for (test, testi) in zip(tests, itertools.count()):
    head = 3 + testi*sizeSize
    ws.cell(1, head, test[0])
    for i in range(sizeFrom, sizeTo + 1):
        ws.cell(2, head + i - sizeFrom, i)
        ws.cell(3, head + i - sizeFrom, '{0:.6g}'.format(numpy.linalg.cond(test[1][i - sizeFrom])))
    ws.merge_cells(start_column=head, start_row=1, end_column=head + sizeSize - 1, end_row=1)
methods = 0
for (module, modulei) in zip(modules, itertools.count()):
    ws.cell(4+methods, 1, module)
    flag = False
    for worker in modules[module]:
        ws.cell(4+methods, 2, re.match(r"<class '.*?\.(.*)'>", str(worker))[1])
        for (testPack, testPacki) in zip(tests, itertools.count()):
            for (A, Ai) in zip(testPack[1], itertools.count()):
                b = [i for i in range(len(A))]
                fun = worker().solve

                # print("A: ", A)
                # print("b: ", b) 
                # print("cond(A)", numpy.linalg.cond(A))
                x = fun(copy.deepcopy(A), copy.deepcopy(b))
                # print("x: ", fun(A, b))
                # print(x)
                ws.cell(4+methods, 3+testPacki*sizeSize+Ai, ' '.join(['{0:.8g}'.format(x) for x in x]))
        methods+=1

wb.save('output.xlsx')