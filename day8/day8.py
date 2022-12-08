#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    trees = [
        list(map(int, line.strip()))
        for line in f
    ]

rowcount = len(trees)
colcount = len(trees[0])

def is_visible_left(row, column):
    global trees
    curtree = trees[row][column]
    for x in range(0, column):
        if curtree <= trees[row][x]:
            return False
    return True

def is_visible_right(row, column):
    global trees, colcount
    curtree = trees[row][column]
    for x in range(column + 1, colcount):
        if curtree <= trees[row][x]:
            return False
    return True

def is_visible_up(row, column):
    global trees
    curtree = trees[row][column]
    for y in range(0, row):
        if curtree <= trees[y][column]:
            return False
    return True

def is_visible_down(row, column):
    global trees, rowcount
    curtree = trees[row][column]
    for y in range(row + 1, rowcount):
        if curtree <= trees[y][column]:
            return False
    return True

def is_visible(r, c):
    return (is_visible_left(r, c)
            or is_visible_up(r, c)
            or is_visible_right(r, c)
            or is_visible_down(r, c))

#visibles = 0
#for row in range(rowcount):
#    for column in range(colcount):
#        if is_visible(row, column):
#            visibles += 1
#
#print(visibles) # part 1

def scenic_score(row, column):
    global trees, rowcount, colcount
    curtree = trees[row][column]
    left = 0
    for x in range(column - 1, -1, -1):
        left += 1
        if curtree <= trees[row][x]:
            break
    up = 0
    for y in range(row - 1, -1, -1):
        up += 1
        if curtree <= trees[y][column]:
            break
    right = 0
    for x in range(column + 1, colcount):
        right += 1
        if curtree <= trees[row][x]:
            break
    down = 0
    for y in range(row + 1, rowcount):
        down += 1
        if curtree <= trees[y][column]:
            break
    return left * up * right * down

print(max(
    max(
        scenic_score(row, column)
        for column in range(colcount))
    for row in range(rowcount))) # part 2
