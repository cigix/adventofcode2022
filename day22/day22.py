#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    lines = list(map(str.rstrip, f))

# get a tuple (x,y) of the position if we were to move right from this position
def goright(x, y):
    newx = x + 1

    # if out of map
    if len(lines[y]) <= newx:
        # position of rightmost space + 1
        # rfind returns -1 if no space => all good
        newx = lines[y].rfind(' ') + 1

    if lines[y][newx] == '#':
        return x, y

    return newx, y

def goleft(x, y):
    newx = x - 1

    if newx < 0 or lines[y][newx] == ' ':
        newx = len(lines[y]) - 1

    if lines[y][newx] == '#':
        return x, y

    return newx, y

def godown(x, y):
    newy = y + 1

    if len(lines) - 2 <= newy:
        newy = 0

    if len(lines[newy]) <= x or lines[newy][x] == ' ':
        newy = 0
    while len(lines[newy]) <= x or lines[newy][x] == ' ':
        newy += 1

    if lines[newy][x] == '#':
        return x, y

    return x, newy

def goup(x, y):
    newy = y - 1

    if newy < 0:
        newy = len(lines) - 3

    if len(lines[newy]) <= x or lines[newy][x] == ' ':
        newy = len(lines) - 3
    while len(lines[newy]) <= x or lines[newy][x] == ' ':
        newy -= 1

    if lines[newy][x] == '#':
        return x, y

    return x, newy

num = None
path = list()
for c in lines[-1]:
    if c.isdigit():
        if num is None:
            num = int(c)
        else:
            num = 10 * num + int(c)
    else:
        if num is not None:
            path.append(num)
            num = None
        path.append(c)
if num is not None:
    path.append(num)

pos = lines[0].rfind(' ') + 1, 0
facing = 0
for motion in path:
    if isinstance(motion, int):
        for _ in range(motion):
            if facing == 0:
                pos = goright(*pos)
            elif facing == 1:
                pos = godown(*pos)
            elif facing == 2:
                pos = goleft(*pos)
            else:
                pos = goup(*pos)
    else:
        if motion == 'R':
            facing += 1
        else:
            facing -= 1
        facing %= 4

print((pos[1] + 1) * 1000 + (pos[0] + 1) * 4 + facing) # part 1
