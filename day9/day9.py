#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    moves = [
        (m, int(c))
        for m, c in map(str.split, map(str.strip, f))]

H = (0, 0)
T = (0, 0)
trace = { T }

def updateT():
    global H, T, trace
    dx = H[0] - T[0]
    dy = H[1] - T[1]
    if -1 <= dx <= 1 and -1 <= dy <= 1:
        # T touches H, no movement
        return
    # Clamp between -1 and 1 => ensures diagonal movement
    dx = max(-1, min(1, dx))
    dy = max(-1, min(1, dy))
    T = T[0] + dx, T[1] + dy
    trace.add(T)

for move, count in moves:
    for _ in range(count):
        if move == 'L':
            H = H[0] - 1, H[1]
        elif move == 'U':
            H = H[0], H[1] - 1
        elif move == 'R':
            H = H[0] + 1, H[1]
        elif move == 'D':
            H = H[0], H[1] + 1
        updateT()

print(len(trace)) # part 1
