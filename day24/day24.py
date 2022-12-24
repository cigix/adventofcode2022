#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    lines = list(map(str.strip, f))

startpos = lines[0].find('.'), 0
endpos = lines[-1].find('.'), len(lines) - 1
blizzards = set()
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c in ">v<^":
            blizzards.add((x, y, c))

step = 0
positions = { startpos }
while True:
    newblizzards = set()
    for x, y, direction in blizzards:
        if direction == '>':
            if lines[y][x + 1] == '#':
                while lines[y][x - 1] != '#':
                    x -= 1
            else:
                x += 1
        elif direction == '<':
            if lines[y][x - 1] == '#':
                while lines[y][x + 1] != '#':
                    x += 1
            else:
                x -= 1
        elif direction == 'v':
            if lines[y + 1][x] == '#':
                while lines[y - 1][x] != '#':
                    y -= 1
            else:
                y += 1
        elif direction == '^':
            if lines[y - 1][x] == '#':
                while lines[y + 1][x] != '#':
                    y += 1
            else:
                y -= 1
        newblizzards.add((x, y, direction))

    newblizzardspositions = set(
        map(
            lambda b: (b[0], b[1]),
            newblizzards))

    newpositions = set()
    for x, y in positions:
        for dx, dy in ((0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)):
            newx, newy = x + dx, y + dy
            if lines[newy][newx] == '#':
                continue # reject that candidate
            if (newx, newy) in newblizzardspositions:
                continue # reject that candidate
            newpositions.add((newx, newy))

    blizzards = newblizzards
    positions = newpositions
    step += 1

    if endpos in newpositions:
        print(step)
        exit(0)
