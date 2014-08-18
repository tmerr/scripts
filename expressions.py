#!python3

"""
Output a massive list of mathematical expressions that produce
the desired output.
"""

import decimal
import sys

# Automatically take care of divisions by zero etc
decimal.setcontext(decimal.ExtendedContext)

class Expression(object):
    __slots__= ['left', 'right']
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Number(Expression):
    __slots__= ['value']
    def __init__(self, value):
        self.value = decimal.Decimal(value)

    def evaluate(self):
        return self.value

    def __str__(self):
        return str(self.value)

class Addition(Expression):
    __slots__ = []
    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()

    def __str__(self):
        return "({0} + {1})".format(self.left, self.right)

class Subtraction(Expression):
    __slots__=  []
    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()

    def __str__(self):
        return "({0} - {1})".format(self.left, self.right)

class Multiplication(Expression):
    __slots__=  []
    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()

    def __str__(self):
        return "({0} * {1})".format(self.left, self.right)

class Division(Expression):
    __slots__=  []
    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()

    def __str__(self):
        return "({0} / {1})".format(self.left, self.right)

class Sqrt(Expression):
    __slots__ = ['subexp']
    def __init__(self, subexp):
        self.subexp = subexp

    def evaluate(self):
        return self.subexp.evaluate().sqrt()

    def __str__(self):
        return "sqrt({0})".format(self.subexp)

def bruteforce(inputs, target, wiggle):
    inputs = [Number(i) for i in inputs]
    target = decimal.Decimal(target)
    wiggle = decimal.Decimal(wiggle)

    expressions = inputs
    generated = inputs
    checker = Checker(target, wiggle)

    while True:
        newgenerated = []
        for g in generated:
            for e in expressions:
                tmp = [
                    Addition(g, e),
                    Subtraction(g, e),
                    Multiplication(g, e),
                    Division(g, e)
                ]
                checker.check(tmp)
                newgenerated.extend(tmp)
            for e in expressions[0:len(expressions) - len(generated)]:
                # Subtraction and division aren't commutative. This matters
                # when the relation is not symmetric. However it is symmetric
                # for the most recently generated elements, so we don't worry
                # about commutivity for those.
                tmp = [
                    Division(e, g),
                    Subtraction(e, g)
                ]
                checker.check(tmp)
                newgenerated.extend(tmp)
        tmp = Sqrt(g)
        checker.check([tmp])
        newgenerated.append(tmp)

        expressions.extend(newgenerated)
        generated = newgenerated

class Checker(object):
    def __init__(self, target, wiggle):
        self.target = target
        self.wiggle = wiggle

    def check(self, lst):
        for i in lst:
            if abs(i.evaluate() - self.target) < self.wiggle:
                print(i)
                sys.stdout.flush()

bruteforce((10, 5, 7), 2.14, .005)
