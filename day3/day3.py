#!/usr/bin/env python

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    rucksacks = list(map(str.strip, f))

def priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27

priorities = 0
for rucksack in rucksacks:
    l = len(rucksack) // 2
    compartments = set(rucksack[:l]), set(rucksack[l:])
    for item in compartments[0] & compartments[1]:
        priorities += priority(item)

#print(priorities) # part 1

badges = 0
for i in range(0, len(rucksacks), 3):
    for badge in set(rucksacks[i]) & set(rucksacks[i + 1]) & set(rucksacks[i + 2]):
        badges += priority(badge)

print(badges) # part 2
