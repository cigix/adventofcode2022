#!/usr/bin/env python3

import itertools
import sys

if len(sys.argv) < 2:
    exit(1)

class Valve:
    def __init__(self, name, rate, tunnels):
        self.name = name # str
        self.rate = rate # int
        self.tunnels = tunnels # list of str

    def __repr__(self):
        return "{ " \
               f"name={self.name:3s} " \
               f"rate={self.rate:3d} "\
               f"tunnels={','.join(self.tunnels)} " \
               "}"

with open(sys.argv[1]) as f:
    lines = list(map(str.strip, f))

valves = dict()
for line in lines:
    s = line.split()
    name = s[1]
    rate = int(s[4][5:-1])
    tunnels = [
        word.strip(',')
        for word in s[9:]
    ]
    valves[name] = Valve(name, rate, tunnels)

# valves that have some relief value
reliefvalves = { valve.name for valve in valves.values() if valve.rate > 0 }

# precomputed distances, from hashes of valve names
distances = { 0: 0 }
def getdistance(src, dst):
    return distances.get(hash(src) ^ hash(dst))
def setdistance(src, dst, dist):
    distances[hash(src) ^ hash(dst)] = dist

def compute_distances_from(src):
    visited = set()
    tovisit = { (src, 0) }
    while tovisit:
        curvalve, distance = tovisit.pop()
        if (d := getdistance(src, curvalve)) is not None:
            if distance < d:
                setdistance(src, curvalve, distance)

        visited.add(curvalve)
        setdistance(src, curvalve, distance)

        for tunnel in valves[curvalve].tunnels:
            if tunnel not in visited:
                tovisit.add((tunnel, distance + 1))

for v in valves.values():
    compute_distances_from(v.name)

maxdist = max(distances.values())

starttime = 30
startvalve = "AA"

class Path:
    # curvalve: str, the valve this Path is currently at
    # relief: int, the relief that was already achieved on this Path
    # openvalves: set of str, the valves that were already opened on this Path
    # remainingtime: int, the time remaining on this path
    # onward: set of str, going towards these valves (prevents backtracking)
    # trace: str, log of the valves
    def __init__(self, curvalve, relief, openvalves, remainingtime, onward, trace):
        self.curvalve = curvalve
        self.relief = relief
        self.openvalves = openvalves
        self.remainingtime = remainingtime
        self.onward = onward
        self.trace = trace

maxrelief = None
def handlestuckpath(path):
    global maxrelief
    if maxrelief is not None and path.relief <= maxrelief:
        return
    print(path.trace, path.relief)
    maxrelief = path.relief

pathqueue = set()
def handlepath(path):
    if path.remainingtime <= 0:
        # no time left to do anything
        handlestuckpath(path)
        return

    lefttoopen = reliefvalves - path.openvalves
    if not lefttoopen:
        # cannot open anymore relief valves
        handlestuckpath(path)
        return

    valve = valves[path.curvalve]

    if path.curvalve in lefttoopen:
        # open this valve
        remainingtime = path.remainingtime - 1
        addedrelief = valve.rate * remainingtime
        pathqueue.add(Path(
            path.curvalve,
            path.relief + addedrelief,
            path.openvalves | { path.curvalve },
            remainingtime,
            None,
            path.trace + " " + path.curvalve))

    if path.onward:
        # We are meant to go somewhere, do not get off that path
        targets = path.onward
    else:
        # We are not set to be going anywhere: let's figure out some targets

        # relief = relief rate * (remaining time - time to get to and open that valve)
        potential_relief = {
            name
            for name, relief in (
                (name, valves[name].rate * (
                    path.remainingtime
                    - getdistance(path.curvalve, name)
                    - 1))
                for name in lefttoopen)
            if relief > 0
        }

        if not potential_relief:
            # no reachable valves with potential to relieve pressure
            handlestuckpath(path)
            return

        targets = potential_relief

    # keys: next tunnel to go to, values: set of valves we are going towards
    next_tunnels = dict()
    # for each target valve
    for target in targets:
        # select the closest tunnel to move to
        mindist = maxdist + 1
        mintunnel = None
        for tunnel in valve.tunnels:
            d = getdistance(tunnel, target)
            if d < mindist:
                mindist = d
                mintunnel = tunnel
        next_tunnels.setdefault(mintunnel, set()).add(target)

    for next_tunnel, onwards in next_tunnels.items():
        pathqueue.add(Path(
            next_tunnel,
            path.relief,
            path.openvalves,
            path.remainingtime - 1,
            onwards,
            path.trace))

pathqueue.add(Path(
    startvalve,
    0,
    set(),
    starttime,
    None,
    ""))
while pathqueue:
    path = pathqueue.pop()
    handlepath(path)

print(maxrelief)
