#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    elves = [0]
    for line in f.readlines():
        if line.strip():
            elves[-1] += int(line.strip())
        else:
            elves.append(0)

print(max(elves))
