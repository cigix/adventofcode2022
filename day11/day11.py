#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

class Monkey:
    # Constant attributes:
    #   - operation: str
    #   - divtest: int
    #   - throwto: 2-uple of int

    # Variable attributes:
    #   - items: list of ints
    #   - activity: int

    def __init__(self, start_items, operation, divtest, truemonkey, falsemonkey):
        self.operation = operation
        self.divtest = divtest
        self.throwto = (falsemonkey, truemonkey)
        self.items = list(start_items)
        self.activity = 0

    def receive_item(self, level):
        self.items.append(level);

    def inspect(self, monkeys, old):
        self.activity += 1
        new = eval(self.operation)
        level = new // 3
        if level % self.divtest == 0:
            monkeys[self.throwto[1]].receive_item(level)
        else:
            monkeys[self.throwto[0]].receive_item(level)

    def round(self, monkeys):
        while self.items:
            self.inspect(monkeys, self.items.pop(0))


with open(sys.argv[1]) as f:
    lines = list(filter(None, map(str.strip, f)))

monkeynum = len(lines) // 6

monkeys = list()
for i in range(monkeynum):
    note = lines[i * 6:(i + 1) * 6]
    start_items = map(int, note[1][16:].split(", "))
    operation = note[2][17:]
    divtest = int(note[3][19:])
    truemonkey = int(note[4][25:])
    falsemonkey = int(note[5][26:])
    monkeys.append(Monkey(start_items, operation, divtest, truemonkey, falsemonkey))


for _ in range(20):
    for monkey in monkeys:
        monkey.round(monkeys)

most_active = sorted(monkey.activity for monkey in monkeys)
print(most_active[-1] * most_active[-2]) # part 1
