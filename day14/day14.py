#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    paths = list(
        map(
            lambda l: list(
                map(eval, l)
                ),
            map(
                lambda s: s.split(" -> "),
                map(
                    str.strip,
                    f
                )
            )
        )
    )

rocks = set()
for path in paths:
    rocks.add(path[0])
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        dx = 1 if start[0] < end[0] else -1 if start[0] > end[0] else 0
        dy = 1 if start[1] < end[1] else -1 if start[1] > end[1] else 0

        cur = start
        while cur != end:
            cur = cur[0] + dx, cur[1] + dy
            rocks.add(cur)
    
lowest = max(map(lambda t: t[1], rocks))
floor = lowest + 1

obstacles = set(rocks)

sandstart = 500, 0
while True:
    sand = sandstart
    for _ in range(floor): # lower at most `floor` times
        candidate = sand[0], sand[1] + 1 # down
        if candidate not in obstacles:
            sand = candidate
            continue
        candidate = sand[0] - 1, sand[1] + 1 # down left
        if candidate not in obstacles:
            sand = candidate
            continue
        candidate = sand[0] + 1, sand[1] + 1 # down right
        if candidate not in obstacles:
            sand = candidate
            continue
        break # no candidates: stop the loop
    # part 1
    #if sand[1] == lowest:
    #    break
    obstacles.add(sand)
    # part 2
    if sand == sandstart:
        break

print(len(obstacles) - len(rocks))

# visualiser
#minx = min(map(lambda t: t[0], obstacles))
#maxx = max(map(lambda t: t[0], obstacles))
#
#for y in range(floor):
#    for dx in range(maxx - minx):
#        pos = minx + dx, y
#        if pos in obstacles:
#            if pos in rocks:
#                print('#', end='')
#            else:
#                print('o', end='')
#        else:
#            print(' ', end='')
#    print()
