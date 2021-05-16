
class Neighbor:
        def __init__(self, edge, left = '', right = ''):
            self.edge = edge
            self.left = left
            self.right = right

class Edge:
    def __init__(self, name, xCoord, yCoord):
       self.name = name
       self.xCoord = xCoord
       self.yCoord = yCoord
       self.neighbors = list()
    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Map:
    def __init__(self, row = 3, column = 4, grid =  [['q', 'v', 'p', 4],['v', 6, 'q', 8], ['p', 'q', 'v', 'v']]):
        self.row = row
        self.column = column
        self.grid = grid
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
                    self.edges[i][j].addNeighbor(neighbor)
                if i+1<=row:
                    neighbor = Neighbor(self.edges[i+1][j])
                    if j>=1:
                        neighbor.right = grid[i][j-1]
                    if j<column:
                        neighbor.left = grid[i][j]
                    self.edges[i][j].addNeighbor(neighbor)
                if j-1>=0:
                    neighbor = Neighbor(self.edges[i][j-1])
                    if i>=1:
                        neighbor.right = grid[i-1][j-1]
                    if i<row:
                        neighbor.left = grid[i][j-1]
                    self.edges[i][j].addNeighbor(neighbor)
                if j+1<=column:
                    neighbor = Neighbor(self.edges[i][j+1])
                    if i>=1:
                        neighbor.left = grid[i-1][j]
                    if i<row:
                        neighbor.right = grid[i][j]
                    self.edges[i][j].addNeighbor(neighbor)
       
    def verifyAdjacency(self, edge1, edge2):
        pass

    def printEdges(self):
       for x in range(len(self.edges)):
           for y in range(len(self.edges[x])):
               print((self.edges[x][y].name), end=', ')
           print('\n')

class AStarPath:
    def __init__(self, map = Map()):
        self.map = map
        self.openList = []
        self.closedList = []
    def calculateCost(self, cur, next):
        pass

class CovidPatient(AStarPath):
    def calculateCost(self, cur, next):
        pass

def main():
    myMap = Map()
    myMap.printEdges()
    for i in range(len(myMap.edges)):
        for j in range(len(myMap.edges[i])):
            edge = myMap.edges[i][j]
            print("Edge: "+edge.name+" has neighbors: ")
            for neighbor in edge.neighbors:
                print("\t"+neighbor.edge.name+" left: "+str(neighbor.left)+", right: "+str(neighbor.right))
            print()

main()