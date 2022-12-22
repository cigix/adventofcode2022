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

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

def turnright(facing):
    return (facing + 1) % 4
def turnleft(facing):
    return (facing - 1) % 4
def opposite(facing):
    return (facing + 2) % 4

pos = lines[0].rfind(' ') + 1, 0
facing = RIGHT
for motion in path:
    if isinstance(motion, int):
        for _ in range(motion):
            if facing == RIGHT:
                pos = goright(*pos)
            elif facing == DOWN:
                pos = godown(*pos)
            elif facing == LEFT:
                pos = goleft(*pos)
            else: # UP
                pos = goup(*pos)
    else:
        if motion == 'R':
            facing = turnright(facing)
        else: # L
            facing = turnleft(facing)

print((pos[1] + 1) * 1000 + (pos[0] + 1) * 4 + facing) # part 1

sidelength = min(map(len, map(str.strip, lines[:-2])))

class Face:
    def __init__(self, x, y):
        global counter
        self.x = x
        self.y = y
        # dict of int (facing) to tuple (Face, int (facing)). See stitch()
        self.stitches = dict()

    def __repr__(self):
        return f"{self.counter}: x={self.x} y={self.y}"

stitchestodo = 12
# stitch 2 faces on their respective sides
def stitch(f1, s1, f2, s2):
    global stitchestodo
    f1.stitches[s1] = (f2, s2)
    f2.stitches[s2] = (f1, s1)
    stitchestodo -= 1

faces = list()
for y in range(0, len(lines) - 2, sidelength):
    for x in range(0, len(lines[y]), sidelength):
        if lines[y][x] != ' ':
            newface = Face(x, y)
            for face in faces:
                if newface.x == face.x and newface.y == face.y + sidelength:
                    stitch(face, DOWN, newface, UP)
                if newface.y == face.y and newface.x == face.x + sidelength:
                    stitch(face, RIGHT, newface, LEFT)
            faces.append(newface)

while 0 < stitchestodo:
    for A in faces:
        # We are at A, trying to find B and C such that A is stitched to B, B is
        # stitched to C, and we could stitch A to C

        for sideAtoB, (B, sideBtoA) in A.stitches.items():
            # Consider:
            # A
            # BC
            # clockwise next side at B
            sideBtoC = turnright(sideBtoA)
            # anticlockwise at A
            sideAtoC = turnleft(sideAtoB)
            # if B is attached to a C, but not A
            if sideBtoC in B.stitches and sideAtoC not in A.stitches:
                C, sideCtoB = B.stitches[sideBtoC]
                # clockwise again
                sideCtoA = turnright(sideCtoB)
                stitch(A, sideAtoC, C, sideCtoA)
                break # A.stitches changed, can't continue this loop
        # only considering "clockwise" ("L") arrangements covers everything,
        # because anticlockwise from A to C is clockwise from C to A

# Exit a face from s1 at relative position dx, dy into side s2 of another face.
# Returns tuple of (int, int) the new relative position
# The new facing is (s2 + 2) % 4
maxd = sidelength - 1
def moveacrossstitch(dx, dy, s1, s2):
    if s1 == RIGHT and s2 == LEFT:
        # exit house right
        return 0, dy
    if s1 == LEFT and s2 == RIGHT:
        # exit house left
        return maxd, dy
    if s1 == DOWN and s2 == UP:
        # jump down from the stage
        return dx, 0
    if s1 == UP and s2 == DOWN:
        # ...ascend out of the stage?
        return dx, maxd

    # 90° clockwise turns
    if s1 == RIGHT and s2 == UP:
        return maxd - dy, 0
    if s1 == DOWN and s2 == RIGHT:
        return maxd, dx
    if s1 == LEFT and s2 == DOWN:
        return maxd - dy, maxd
    if s1 == UP and s2 == LEFT:
        return 0, dx

    # 90° anticlockwise turns
    if s1 == LEFT and s2 == UP:
        return dy, 0
    if s1 == DOWN and s2 == LEFT:
        return 0, maxd - dx
    if s1 == RIGHT and s2 == DOWN:
        return dy, maxd
    if s1 == UP and s2 == RIGHT:
        return maxd, maxd - dx

    # weird shit beyond this point
    if s1 == RIGHT: # s2 == RIGHT
        return maxd, maxd - dy
    if s1 == LEFT: # s2 == LEFT
        return 0, maxd - dy
    if s1 == DOWN: # s2 == DOWN
        return maxd - dx, maxd
    #s1 == UP and s2 == UP
    return maxd - dx, 0

# From a relative position on one face, attempt moving to another face
# Returns: tuple of (Face, int, int, int), the new face, relative position, and
#   heading (may be same as inputs if blocked by a wall)
def goaccross(face, dx, dy, facing):
    newface, toside = face.stitches[facing]
    newdx, newdy = moveacrossstitch(dx, dy, facing, toside)
    # we face the opposite of the side we are arriving from
    return newface, newdx, newdy, opposite(toside)

curface = faces[0]
dx, dy = 0, 0
facing = RIGHT
for motion in path:
    if isinstance(motion, int):
        for _ in range(motion):
            if facing == RIGHT:
                if dx == maxd: # can't go more right
                    newface, newdx, newdy, newfacing = \
                            goaccross(curface, dx, dy, facing)
                else:
                    newface, newdx, newdy, newfacing = \
                            curface, dx + 1, dy, facing
            elif facing == DOWN:
                if dy == maxd: # can't go more down
                    newface, newdx, newdy, newfacing = \
                            goaccross(curface, dx, dy, facing)
                else:
                    newface, newdx, newdy, newfacing = \
                            curface, dx, dy + 1, facing
            elif facing == LEFT:
                if dx == 0: # can't go more left
                    newface, newdx, newdy, newfacing = \
                            goaccross(curface, dx, dy, facing)
                else:
                    newface, newdx, newdy, newfacing = \
                            curface, dx - 1, dy, facing
            else: # facing == UP
                if dy == 0: # can't go more up
                    newface, newdx, newdy, newfacing = \
                            goaccross(curface, dx, dy, facing)
                else:
                    newface, newdx, newdy, newfacing = \
                            curface, dx, dy - 1, facing

            x, y = newface.x + newdx, newface.y + newdy
            if lines[y][x] != '#':
                curface, dx, dy, facing = newface, newdx, newdy, newfacing
    else:
        if motion == 'R':
            facing = turnright(facing)
        else: # L
            facing = turnleft(facing)

x, y = curface.x + dx, curface.y + dy
print((y + 1) * 1000 + (x + 1) * 4 + facing) # part 2
