import Map as mp
import numpy as np
from enum import Enum

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    DOWN_RIGHT = 4
    DOWN_LEFT = 5
    UP_LEFT = 6
    UP_RIGHT = 7

    def __str__(self):
        if self.value == 0:
            return str('RIGHT')
        if self.value == 1:
            return str('DOWN')
        if self.value == 2:
            return str('LEFT')
        if self.value == 3:
            return str('UP')
        return str()

class Node():
    def __init__(self, edges):
        self.edges: list[Edge] = edges

class Edge():
    def __init__(self,name: str, node1: Node, node2: Node, zoneLeft: Zone, zoneRight: Zone):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.zoneLeft = zoneLeft
        self.zoneRight = zoneRight


class Zone():
    def __init__(self, x: int, y: int, zType: str):
        self.x = x
        self.y = y
        self.zType = zType
        self.ulNode: Edge = None
        self.urNode: Edge = None
        self.drNode: Edge = None
        self.dlNode: Edge = None

class Map:
    def __init__(self, row = 3, column = 4, gridData =  [['q', 'v', 'p', ' '],['v', ' ', 'q', ' '], ['p', 'q', 'v', 'v']]):
        self.row = row
        self.column = column
        self.zones = list()

        # Generate the grid of zones
        for i in range(len(gridData)):
            self.zones.append(list())
            for j in range(len(gridData[i])):
                self.zones[i].append(Zone(j, i, gridData[i][j]))
            self.zones[i] = np.array(self.zones[i])
        self.zones = np.array(self.zones)

        # Generate the edges
        edges = list(list())
        x = 65
        for i in range(row+1):
            edges.append(list())
            for j in range(column+1):
                edge = Edge(chr(x), i, j)
                edges[i].append(edge)
                x+=1

        # Now to set the zone to edge relationships
        zone: Zone
        edge: Edge
        for i in range(len(self.zones)):
            for j in range(len(self.zones[i])):
                zone = self.zones[i][j]
                # First et the upperleft edge
                edge = edges[i][j]
                zone.ulEdge = edge
                edge.drZone = zone
                # Next Set the upperright edge
                edge = edges[i][j+1]
                zone.urEdge = edge
                edge.dlZone = zone
                # Next the downright edge
                edge = edges[i+1][j+1]
                zone.drEdge = edge
                edge.ulZone = zone
                # Finally the downleft edge
                edge = edges[i+1][j]
                zone.dlEdge = edge
                edge.urZone = zone


    def __str__(self):
        zone: Zone
        edge: Edge
        s: str = str("Here is your map: \n")
        for i in range(self.row):
            for j in range(self.column):
                s+=str(self.zones[i][j].ulEdge.name)+"\t\t"
            s+=self.zones[i][j].urEdge.name+"\n"
            s+="\n\t"
            for j in range(self.column):
                s+="*"+self.zones[i][j].zType+"*\t\t"
            s+="\n\n"
        for j in range(self.column):
            s+=self.zones[i][j].dlEdge.name+"\t\t"
        s+=self.zones[self.row-1][self.column-1].drEdge.name
        return s


def CalcCostC(start: Edge, dir: Direction):
    cost = 0.0
    left = None
    right = None
    if dir == Direction.RIGHT:
        if start.urZone is not None:
            left = start.urZone.zType
        if start.drZone is not None:
            right = start.drZone.zType
    if dir == Direction.DOWN:
        if start.dlZone is not None:
            left = start.dlZone.zType
        if start.drZone is not None:
            right = start.drZone.zType
    if dir == Direction.LEFT:
        if start.dlZone is not None:
            left = start.dlZone.zType
        if start.urZone is not None:
            right = start.urZone.zType
    if dir == Direction.UP:
        if start.ulZone is not None:
            left = start.ulZone.zType
        if start.urZone is not None:
            right = start.urZone.zType
    switcher = {
        'q': 0,
        'v': 2,
        'p': 3,
        ' ': 1}
    if left is not None and right is not None:
        cost = (switcher.get(left) + switcher.get(right))*0.5
    elif left is not None:
        cost = switcher.get(left)
    elif right is not None:
        cost = switcher.get(right)
    return cost
    



def main():
   # mp.printMap()
    map = Map()  
    print(map)
    for x in map.zones:
        for y in x:
            print(y)

    #print("edges equal? : "+str(z1.urEdge == z2.urEdge))
    print("A->B: "+str(CalcCostC(map.zones[0][0].ulEdge, Direction.RIGHT)))
    print("B->C: "+str(CalcCostC(map.zones[0][1].ulEdge, Direction.RIGHT)))
    print("C->D: "+str(CalcCostC(map.zones[0][2].ulEdge, Direction.RIGHT)))
    print("D->E: "+str(CalcCostC(map.zones[0][3].ulEdge, Direction.RIGHT)))
    print("B->G: "+str(CalcCostC(map.zones[0][1].ulEdge, Direction.DOWN)))
    print("C->H: "+str(CalcCostC(map.zones[0][2].ulEdge, Direction.DOWN)))



main()