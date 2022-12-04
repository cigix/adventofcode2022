#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

groups = list() # list of 2-uple of 2-uple of int
with open(sys.argv[1]) as f:
    for line in f:
        ranges = line.strip().split(',')
        groups.append(tuple(
            tuple(map(int, r.split('-')))
            for r in ranges))

def full_overlap(r1, r2):
    if r1[0] <= r2[0] and r2[1] <= r1[1]:
        # r1 overlaps r2
        return True
    elif r2[0] <= r1[0] and r1[1] <= r2[1]:
        # r2 overlaps r1
        return True
    return False

full_overlaps = 0
for ranges in groups:
    if full_overlap(*ranges):
        full_overlaps += 1

#print(full_overlaps) # part 1

def overlap(r1, r2):
    if r1[0] <= r2[0]:
        # r1 starts before r2: overlap if r2 starts before r1 ends
        return r2[0] <= r1[1]
    else:
        # r2 starts before r1: overlap if r1 starts before r2 ends
        return r1[0] <= r2[1]

overlaps = 0
for ranges in groups:
    if overlap(*ranges):
        overlaps += 1

print(overlaps) # part 2
