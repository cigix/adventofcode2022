#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    lines = list(f)

i = 0
while lines[i] != "\n":
    i += 1

crates, procedures = lines[:i], lines[i + 1:]

stacks_len = len(crates[0]) // 4 # per crate: 3 chars + 1 space or LF
stacks = [list() for _ in range(stacks_len)]
for row in crates[:-1]:
    for column in range(stacks_len):
        c = row[column * 4 + 1]
        if c != ' ':
            stacks[column].insert(0, c)

for procedure in procedures:
    s = procedure.strip().split()
    quantity = int(s[1])
    source = int(s[3]) - 1
    destination = int(s[5]) - 1
    # part 1
    #for _ in range(quantity):
    #    stacks[destination].append(stacks[source].pop())
    # part 2
    stacks[destination].extend(stacks[source][-quantity:])
    del stacks[source][-quantity:]

print(''.join(map(lambda x: x[-1], stacks)))
