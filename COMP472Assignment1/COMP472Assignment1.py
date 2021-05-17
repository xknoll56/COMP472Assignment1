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
    def __init__(self,name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y
        self.ulZone: Zone = None
        self.urZone: Zone = None
        self.drZone: Zone = None
        self.dlZone: Zone = None

    def __str__(self):
        s: str = ""
        s+= "Node: "+self.name+" has coordinates ("+self.x+","+self.y+") and surrounding zones: \n"
        s+="\t Upper Left Zone: "+self.ulZone.zType
        s+="\t Upper Right Zone: "+self.ueZonw.zType
        s+="\t Down Left Zone: "+self.dlZonee
        s+="\t Down Right Zone: "+self.drZone.zType
        return s

class Zone():
    def __init__(self, x: int, y: int, zType: str):
        self.x = x
        self.y = y
        self.zType = zType
        self.ulNode: Node = None
        self.urNode: Node = None
        self.drNode: Node = None
        self.dlNode: Node = None

    def __str__(self):
        s: str = ""
        s += "Zone has type: "+self.zType+" and coordinates: ("+str(self.x)+","+str(self.y)+") and has Nodes: \n"
        s += "\t Upper left Node: "+self.ulNode.name + "\n"
        s += "\t Upper Right Node: "+self.urNode.name+ "\n"
        s += "\t Down left Node: "+self.dlNode.name+ "\n"
        s += "\t Down Right Node: "+self.drNode.name
        return s

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

        # Generate the Nodes
        Nodes = list(list())
        x = 65
        for i in range(row+1):
            Nodes.append(list())
            for j in range(column+1):
                node = Node(chr(x), i, j)
                Nodes[i].append(Node)
                x+=1

        # Now to set the zone to Node relationships
        zone: Zone
        Node: Node
        for i in range(len(self.zones)):
            for j in range(len(self.zones[i])):
                zone = self.zones[i][j]
                # First et the upperleft Node
                Node = Nodes[i][j]
                zone.ulNode = Node
                Node.drZone = zone
                # Next Set the upperright Node
                Node = Nodes[i][j+1]
                zone.urNode = Node
                Node.dlZone = zone
                # Next the downright Node
                Node = Nodes[i+1][j+1]
                zone.drNode = Node
                Node.ulZone = zone
                # Finally the downleft Node
                Node = Nodes[i+1][j]
                zone.dlNode = Node
                Node.urZone = zone


    def __str__(self):
        zone: Zone
        Node: Node
        s: str = str("Here is your map: \n")
        for i in range(self.row):
            for j in range(self.column):
                s+=str(self.zones[i][j].ulNode.name)+"\t\t"
            s+=self.zones[i][j].urNode.name+"\n"
            s+="\n\t"
            for j in range(self.column):
                s+="*"+self.zones[i][j].zType+"*\t\t"
            s+="\n\n"
        for j in range(self.column):
            s+=self.zones[i][j].dlNode.name+"\t\t"
        s+=self.zones[self.row-1][self.column-1].drNode.name
        return s


def CalcCostC(start: Node, dir: Direction):
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

    #print("Nodes equal? : "+str(z1.urNode == z2.urNode))
    print("A->B: "+str(CalcCostC(map.zones[0][0].ulNode, Direction.RIGHT)))
    print("B->C: "+str(CalcCostC(map.zones[0][1].ulNode, Direction.RIGHT)))
    print("C->D: "+str(CalcCostC(map.zones[0][2].ulNode, Direction.RIGHT)))
    print("D->E: "+str(CalcCostC(map.zones[0][3].ulNode, Direction.RIGHT)))
    print("B->G: "+str(CalcCostC(map.zones[0][1].ulNode, Direction.DOWN)))
    print("C->H: "+str(CalcCostC(map.zones[0][2].ulNode, Direction.DOWN)))



main()