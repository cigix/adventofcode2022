#!/usr/bin/env python

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    rucksacks = list(map(str.strip, f))

priorities = 0
for rucksack in rucksacks:
    l = len(rucksack) // 2
    compartments = set(rucksack[:l]), set(rucksack[l:])
    for item in compartments[0] & compartments[1]:
        if item.islower():
            priorities += ord(item) - ord('a') + 1
        else:
            priorities += ord(item) - ord('A') + 27

print(priorities) # part 1
