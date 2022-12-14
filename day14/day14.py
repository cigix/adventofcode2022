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

sands = set()

sandstart = 500, 0
while True:
    sand = sandstart
    for _ in range(lowest): # lower at most `lowest` times
        candidate = sand[0], sand[1] + 1 # down
        if candidate not in (rocks | sands):
            sand = candidate
            continue
        candidate = sand[0] - 1, sand[1] + 1 # down left
        if candidate not in (rocks | sands):
            sand = candidate
            continue
        candidate = sand[0] + 1, sand[1] + 1 # down right
        if candidate not in (rocks | sands):
            sand = candidate
            continue
        break # no candidates: stop the loop
    if sand[1] == lowest:
        break
    sands.add(sand)

print(len(sands))
