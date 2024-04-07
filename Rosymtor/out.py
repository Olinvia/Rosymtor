import os
import io
from collections import OrderedDict

path = 'prim_bwd.train'
tan = "tan"
assert os.path.isfile(path)

variables = ['x', 'y', 'z', 't']
coefficients = [f'a{i}' for i in range(10)]
constants = ['pi', 'E']
OPERATORS = {
    # Elementary functions
    'add': 2,
    'sub': 2,
    'mul': 2,
    'div': 2,
    'pow': 2,
    'rac': 2,
    'inv': 1,
    'pow2': 1,
    'pow3': 1,
    'pow4': 1,
    'pow5': 1,
    'sqrt': 1,
    'exp': 1,
    'ln': 1,
    'abs': 1,
    'sign': 1,
    # Trigonometric Functions
    'sin': 1,
    'cos': 1,
    'tan': 1,
    'cot': 1,
    'sec': 1,
    'csc': 1,
    # Trigonometric Inverses
    'asin': 1,
    'acos': 1,
    'atan': 1,
    'acot': 1,
    'asec': 1,
    'acsc': 1,
    # Hyperbolic Functions
    'sinh': 1,
    'cosh': 1,
    'tanh': 1,
    'coth': 1,
    'sech': 1,
    'csch': 1,
    # Hyperbolic Inverses
    'asinh': 1,
    'acosh': 1,
    'atanh': 1,
    'acoth': 1,
    'asech': 1,
    'acsch': 1,
    # Derivative
    'derivative': 2,
    # custom functions
    'f': 1,
    'g': 2,
    'h': 3,
}


def conv(expr):
    tann = "tan"
    words = expr.split(' ')
    while tann in words:
        index = words.index(tann)
        i = index + 1
        count = 1
        while i < len(words):
            if words[i] in variables:
                count = count - 1
            elif words[i] in coefficients:
                count = count - 1
            elif words[i] in constants:
                count = count - 1
            elif words[i] == 'INT-' or words[i] == 'INT+':
                count = count - 1
                i = i + 1
                while i < len(words) and words[i].isdigit():
                    i = i + 1
                i = i - 1
            elif words[i] in OPERATORS.keys():
                count = count + OPERATORS[words[i]] - 1
            else:
                print(words[i])
                print('wrong!')
                break

            if count == 0:
                break

            i = i + 1

        words = words[:index] + ['div', 'sin'] + words[index+1:i+1] + ['cos'] + words[index+1:i+1] + words[i+1:]

    expr_n = ' '.join(words)
    return expr_n


lines = []
with io.open(path, mode='r', encoding='utf-8') as f:  # 打开文件
    for i, line in enumerate(f):
        lines.append(line.rstrip().split('|'))
data = [xy.split('\t') for _, xy in lines]
data = [xy for xy in data if len(xy) == 2]

file_handler_prefix = io.open('./conv.train', mode='a', encoding='utf-8')

for i in range(len(data)):
    x, y = data[i]
    x = conv(x)
    y = conv(y)
    file_handler_prefix.write(f'{x}\t{y}\n')
    file_handler_prefix.flush()


