import numpy as np
from enum import Enum

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

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

class Neighbor:
        def __init__(self, edge, left = 'oob', right = 'oob', dir = Direction.RIGHT):
            self.edge = edge
            self.left = left
            self.right = right
            self.direction = dir

class Edge:
    def __init__(self, name, xCoord, yCoord):
       self.name = name
       self.xCoord = xCoord
       self.yCoord = yCoord
       self.neighbors: list[Neighbor] = list()
    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Map:
    def __init__(self, row = 3, column = 4, grid =  [['q', 'v', 'p', ' '],['v', ' ', 'q', ' '], ['p', 'q', 'v', 'v']]):
        self.row = row
        self.column = column
        self.grid = np.array(grid)
        self.edges = list(list())
        x = 65
        for i in range(row+1):
            self.edges.append(list())
            for j in range(column+1):
                edge = Edge(chr(x), i, j)
                self.edges[i].append(edge)
                x+=1
        for i in range(row+1):
            for j in range(column+1):
                if i-1>=0:
                    neighbor = Neighbor(self.edges[i-1][j])
                    if j>=1:
                        neighbor.left = grid[i-1][j-1]
                    if j<column:
                        neighbor.right = grid[i-1][j]
                    neighbor.direction = Direction.UP
                    self.edges[i][j].addNeighbor(neighbor)
                if i+1<=row:
                    neighbor = Neighbor(self.edges[i+1][j])
                    if j>=1:
                        neighbor.right = grid[i][j-1]
                    if j<column:
                        neighbor.left = grid[i][j]
                    neighbor.direction = Direction.DOWN
                    self.edges[i][j].addNeighbor(neighbor)
                if j-1>=0:
                    neighbor = Neighbor(self.edges[i][j-1])
                    if i>=1:
                        neighbor.right = grid[i-1][j-1]
                    if i<row:
                        neighbor.left = grid[i][j-1]
                    neighbor.direction = Direction.LEFT
                    self.edges[i][j].addNeighbor(neighbor)
                if j+1<=column:
                    neighbor = Neighbor(self.edges[i][j+1])
                    if i>=1:
                        neighbor.left = grid[i-1][j]
                    if i<row:
                        neighbor.right = grid[i][j]
                    neighbor.direction = Direction.RIGHT
                    self.edges[i][j].addNeighbor(neighbor)
       

    def printEdges(self):
       for x in range(len(self.edges)):
           for y in range(len(self.edges[x])):
               print((self.edges[x][y].name), end='\t\t')
           if x<len(self.edges)-1:
               print('\n', end ='\t')              
               for y in range(len(self.edges[x])-1):
                   print("**"+str(self.grid[x][y])+"**", end = '\t\t')
           print("")


class AStarPath:
    def __init__(self, map=Map()):
        self.map = map
        self.openList = []
        self.closedList = []
    def calculateCost(self, cur, next):
        pass

class CovidPatient(AStarPath):
    def calculateCost(self, cur, next):
        cost = 0
        for neighbor in cur.neighbors:
            if neighbor.edge == next:
                #print(neighbor.direction)
                left = neighbor.left
                right = neighbor.right
                if left == 'q':
                    cost += 0
                elif left == 'v':
                    cost += 2
                elif left == 'p':
                    cost += 3
                elif left == ' ':
                    cost += 1
                if right == 'q':
                    cost += 0
                elif right == 'v':
                    cost += 2
                elif right == 'p':
                    cost += 3
                elif right == ' ':
                    cost += 1
                if left == 'oob' or right == 'oob':
                    pass
                else: 
                    cost *= 0.5
        return float(cost)
                

def printMap():
    myMap = Map()
    myMap.printEdges()
    for listEdges in myMap.edges:
        for edge in listEdges:
            print("Edge: " + edge.name + " has neighbors: ")
            for neighbor in edge.neighbors:
                print("\t" + neighbor.edge.name + " left: " + str(neighbor.left) + ", right: " + str(neighbor.right))
            print()
    c = CovidPatient(myMap)
    print("A->B: " + str(c.calculateCost(myMap.edges[0][0], myMap.edges[0][1])))
    print("B->C: " + str(c.calculateCost(myMap.edges[0][1], myMap.edges[0][2])))
    print("C->D: " + str(c.calculateCost(myMap.edges[0][2], myMap.edges[0][3])))
    print("D->E: " + str(c.calculateCost(myMap.edges[0][3], myMap.edges[0][4])))
    print("B->G: " + str(c.calculateCost(myMap.edges[0][1], myMap.edges[1][1])))
    print("C->H: " + str(c.calculateCost(myMap.edges[0][2], myMap.edges[1][2])))

