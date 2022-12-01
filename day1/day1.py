#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

elves = [0]
with open(sys.argv[1]) as f:
    for line in f.readlines():
        if line.strip():
            elves[-1] += int(line.strip())
        else:
            elves.append(0)

#print(max(elves)) # part 1

elves = sorted(elves)
print(sum(elves[-3:])) # part 2
