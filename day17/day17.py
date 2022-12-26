#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    jets = f.read().strip()

def addt(*tuples):
    return tuple(map(sum, zip(*tuples)))

class Shape:
    # width: int, number of columns spanned
    # offsets: frozenset of tuples of (int, int), the set of offsets
    def __init__(self, *offsets):
        self.width = 1 + max(map(lambda t: t[0], offsets))
        self.offsets = frozenset(offsets)

# mapping of name to Shape
shapes = {
    '-': Shape(
        (0, 0), (1, 0), (2, 0), (3, 0)
        ),
    '+': Shape(
                (1, 2),
        (0, 1), (1, 1), (2, 1),
                (1, 0)
    ),
    'J': Shape(
                        (2, 2),
                        (2, 1),
        (0, 0), (1, 0), (2, 0)
    ),
    '|': Shape(
        (0, 3),
        (0, 2),
        (0, 1),
        (0, 0)
    ),
    'o': Shape(
        (0, 1), (1, 1),
        (0, 0), (1, 0)
    )
}

def repeatgenerator(iterable):
    while True:
        for item in iterable:
            yield item

jetgenerator = repeatgenerator(jets)
shapegenerator = repeatgenerator("-+J|o")

maxwidth = 7
occupied = set()
heightmap = [0] * maxwidth
for _ in range(2022):
    # position of the lower left corner of the new shape
    x = 2
    y = max(heightmap) + 3

    shapename = next(shapegenerator)
    shape = shapes[shapename]
    shapeoccupies = {
        addt((x, y), offset)
        for offset in shape.offsets
    }

    while True:
        # attempt sideways movement
        jet = next(jetgenerator)
        if jet == '<':
            if 0 < x:
                shapewouldoccupy = {
                    addt((-1, 0), position)
                    for position in shapeoccupies
                }
                if not shapewouldoccupy & occupied:
                    x -= 1
                    shapeoccupies = shapewouldoccupy
        else: # jet == '>'
            if x + shape.width < maxwidth:
                shapewouldoccupy = {
                    addt((1, 0), position)
                    for position in shapeoccupies
                }
                if not shapewouldoccupy & occupied:
                    x += 1
                    shapeoccupies = shapewouldoccupy

        # attempt downwards movement
        if y == 0:
            break
        shapewouldoccupy = {
            addt((0, -1), position)
            for position in shapeoccupies
        }
        if shapewouldoccupy & occupied:
            break
        y -= 1
        shapeoccupies = shapewouldoccupy

    occupied |= shapeoccupies

    for x, y in shapeoccupies:
        if heightmap[x] <= y:
            heightmap[x] = y + 1

print(max(heightmap))
