#!/usr/bin/env python3

import itertools
import sys

if len(sys.argv) < 2:
    exit(1)

class Valve:
    # name: str
    # rate: int
    # tunnels: set of str
    def __init__(self, name, rate, tunnels):
        self.name = name
        self.rate = rate
        self.tunnels = tunnels

valves = dict()
with open(sys.argv[1]) as f:
    for line in f:
        words = line.strip().split()
        name = words[1]
        rate = int(words[4][5:-1])
        tunnels = {
            word.strip(',')
            for word in words[9:]
        }
        valves[name] = Valve(name, rate, tunnels)

# valves with some relief value
reliefvalves = {
    valve.name
    for valve in valves.values()
    if valve.rate > 0
}

# we enforce symmetric and minimal distances
distances = { 0: 0 }
def getdistance(src, dst):
    return distances.get(hash(src) ^ hash(dst))
def setdistance(src, dst, distance):
    k = hash(src) ^ hash(dst)
    d = distances.get(k)
    if d is None or distance < d:
        distances[k] = distance
        return True
    return False

# precompute all distances
for src in valves.values():
    visited = set()
    tovisit = { (src.name, 0) }
    while tovisit:
        curname, distance = tovisit.pop()
        setdistance(src.name, curname, distance)
        visited.add(curname)
        for tunnel in valves[curname].tunnels - visited:
            tovisit.add((tunnel, distance + 1))

class State:
    # name: str, the name of the valve this State is currently on
    # relief: int, the relief already achieved on this State
    # opened: frozenset of str, the valves that were opened in this State
    # remaining: int, the remaining time
    def __init__(self, name, relief, opened, remaining):
        self.name = name
        self.relief = relief
        self.opened = opened
        self.remaining = remaining

def getmaxreliefs(start, maxtime):
    # mapping from sets of open valves to achievable reliefs
    maxreliefs = dict()

    def setmaxrelief(state):
        key = state.opened
        maxreliefs[key] = max(
            maxreliefs.get(key, 0),
            state.relief
        )

    todo = { State(start, 0, frozenset(), maxtime) }
    while todo:
        state = todo.pop()

        # what if we stopped here?
        setmaxrelief(state)

        # for each unopened relief valve
        for name in reliefvalves - state.opened:
            # simulate going to and opening that valve
            remaining = state.remaining - getdistance(state.name, name) - 1
            if 0 < remaining:
                relief = state.relief + valves[name].rate * remaining
                opened = state.opened | { name }
                todo.add(State(name, relief, opened, remaining))

    return maxreliefs

print(max(getmaxreliefs("AA", 30).values())) # part 1

# part 2
maxreliefs = getmaxreliefs("AA", 26)
# Take all combinations of pairs of sets of open valves, keep the disjoint ones,
# compute the maximum of the maximum possible reliefs of opening those sets.
print(max(
    map(
        lambda t: maxreliefs[t[0]] + maxreliefs[t[1]],
        filter(
            lambda t: t[0].isdisjoint(t[1]),
            itertools.combinations(
                maxreliefs.keys(),
                2
            )
        )
    )
))
