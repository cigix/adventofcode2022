#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    moves = [
        (m, int(c))
        for m, c in map(str.split, map(str.strip, f))]

knots = [(0, 0)] * 10

# update knots[k] from knots[k - 1]
def updateKnot(k):
    global knots
    dx = knots[k - 1][0] - knots[k][0]
    dy = knots[k - 1][1] - knots[k][1]
    if -1 <= dx <= 1 and -1 <= dy <= 1:
        # knots[k] touches knots[k - 1], no movement
        return
    # Clamp between -1 and 1 => ensures diagonal movement
    dx = max(-1, min(1, dx))
    dy = max(-1, min(1, dy))
    knots[k] = knots[k][0] + dx, knots[k][1] + dy

trace1 = { knots[1] }
traceT = { knots[-1] }
for move, count in moves:
    for _ in range(count):
        if move == 'L':
            knots[0] = knots[0][0] - 1, knots[0][1]
        elif move == 'U':
            knots[0] = knots[0][0], knots[0][1] - 1
        elif move == 'R':
            knots[0] = knots[0][0] + 1, knots[0][1]
        elif move == 'D':
            knots[0] = knots[0][0], knots[0][1] + 1
        for k in range(1, len(knots)):
            updateKnot(k)
        trace1.add(knots[1])
        traceT.add(knots[-1])

print(len(trace1)) # part 1
print(len(traceT)) # part 2
