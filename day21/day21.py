#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

class Expr:
    # isconstant() -> bool
    # value() -> int
    pass

class ValueExpr(Expr):
    def __init__(self, value):
        self._value = value

    def isconstant(self):
        return True

    def value(self):
        return self._value

    def __repr__(self):
        return repr(self._value)

class OpExpr(Expr):
    # op: str
    # lhs: Expr
    # rhs: Expr
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
        self._isconstant = None

    def isconstant(self):
        if self._isconstant is None:
            self._isconstant = self.lhs.isconstant() and self.rhs.isconstant()
        return self._isconstant

    def value(self):
        lhs = self.lhs.value()
        rhs = self.rhs.value()
        return eval(f"{lhs} {self.op} {rhs}")

    def __repr__(self):
        return f"({self.lhs} {self.op} {self.rhs})"

class HumanExpr(Expr):
    def isconstant(self):
        return False

    def __repr__(self):
        return "human"

class Monkey:
    # value(dict) -> int
    # toexpr(dict) -> Expr
    pass

class ValueMonkey(Monkey):
    def __init__(self, value):
        self._value = value

    def value(self, _):
        return self._value

    def toexpr(self, _):
        return ValueExpr(self._value)

class OpMonkey(Monkey):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = "//" if op == "/" else op
        self.rhs = rhs
        self._value = None

    def value(self, monkeydict):
        if self._value is None:
            lhsvalue = monkeydict[self.lhs].value(monkeydict)
            rhsvalue = monkeydict[self.rhs].value(monkeydict)
            self._value = eval(f"{lhsvalue} {self.op} {rhsvalue}")
        return self._value

    def toexpr(self, monkeydict):
        lhs = monkeydict[self.lhs].toexpr(monkeydict)
        rhs = monkeydict[self.rhs].toexpr(monkeydict)
        return OpExpr(lhs, self.op, rhs)

class Human(ValueMonkey):
    def toexpr(_, __):
        return HumanExpr()

monkeydict = dict()
with open(sys.argv[1]) as f:
    for line in f:
        name, job = line.split(':')
        job = job.strip()
        if name == "humn":
            monkeydict[name] = Human(int(job))
        elif job.isdigit():
            monkeydict[name] = ValueMonkey(int(job))
        else:
            monkeydict[name] = OpMonkey(*job.split())

print(monkeydict["root"].value(monkeydict)) # part 1

root = monkeydict["root"].toexpr(monkeydict)
root.op = "=="
# put human on the leftmost side
if not root.rhs.isconstant():
    root.lhs, root.rhs = root.rhs, root.lhs
print(root)

while not isinstance(root.lhs, HumanExpr):
    a = root.lhs.lhs # maybe constant
    op = root.lhs.op
    b = root.lhs.rhs # maybe constant
    c = root.rhs # constant

    # keep constants on the right
    if op == '+':
        if b.isconstant():
            # a + b = c => a = c - b
            newlhs = a
            newrhs = OpExpr(c, '-', b)
        else:
            # a + b = c => b = c - a
            newlhs = b
            newrhs = OpExpr(c, '-', a)
    elif op == '-':
        if b.isconstant():
            # a - b = c => a = c + b
            newlhs = a
            newrhs = OpExpr(c, '+', b)
        else:
            # a - b = c => b = a - c
            newlhs = b
            newrhs = OpExpr(a, '-', c)
    elif op == '*':
        if b.isconstant():
            # a * b = c => a = c / b
            newlhs = a
            newrhs = OpExpr(c, "//", b)
        else:
            # a * b = c => b = c / a
            newlhs = b
            newrhs = OpExpr(c, "//", a)
    elif op == "//":
        if b.isconstant():
            # a / b = c => a = c * b
            newlhs = a
            newrhs = OpExpr(c, '*', b)
        else:
            # a / b = c => b = a / c
            newlhs = b
            newrhs = OpExpr(a, "//", c)

    root.lhs = newlhs
    root.rhs = newrhs
    print(root)
print(root.rhs.value())
