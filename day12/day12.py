#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    lines = list(map(str.strip, f))

start = None
end = None
for i, line in enumerate(lines):
    if 'S' in line:
        start = (line.index('S'), i)
        lines[i] = lines[i].replace('S', 'a')
    if 'E' in line:
        end = (line.index('E'), i)
        lines[i] = lines[i].replace('E', 'z')

rowcount = len(lines)
colcount = len(lines[0])
m = rowcount * colcount + 1

distances = [
    [m] * colcount
    for _ in range(rowcount)
]

#distances[start[1]][start[0]] = 0 # part 1
distances[end[1]][end[0]] = 0 # part 2

#queue = [start] # part 1
queue = [end] # part 2
while queue:
    col, row = queue.pop(0)

    # part 1
    #if (col, row) == end:
    #    break

    distance = distances[row][col]
    altitude = ord(lines[row][col])

    # part 2
    if altitude == ord('a'):
        newstart = (col, row)
        break

    def consider_neighbor(dx, dy):
        ncol = col + dx
        nrow = row + dy
        if not (0 <= ncol < colcount and 0 <= nrow < rowcount):
            return
        naltitude = ord(lines[nrow][ncol])
        # if more than 1 higher altitude
        #if altitude + 1 < naltitude: # part 1
        if naltitude + 1 < altitude: # part 2
            return
        ndistance = distances[nrow][ncol]
        if ndistance <= distance + 1:
            return

        # in bounds, <= 1 altitude change, not accessible quicker
        distances[nrow][ncol] = distance + 1
        queue.append((ncol, nrow))

    consider_neighbor(0, 1) # up
    consider_neighbor(1, 0) # right
    consider_neighbor(0, -1) # down
    consider_neighbor(-1, 0) # left

#print(distances[end[1]][end[0]]) # part 1
print(distances[newstart[1]][newstart[0]]) # part 2
