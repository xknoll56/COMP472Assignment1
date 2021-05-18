import numpy as np

class Node():
    pass
class Edge():
    pass
class Zone():
    pass



class Node():
    def __init__(self, name: str, x:int, y:int):
        self.name: str = name
        self.x = x
        self.y = y
        self.edges: list[Edge] = list()
        #Edge to the Right
        self.rEdge: Edge = None
        #Edge to Downward
        self.dEdge: Edge = None
        #Edge to the Left
        self.lEdge: Edge = None
        #Edge to Upward
        self.uEdge: Edge = None
        self.prevNode: Node = None

class Edge():
    def __init__(self, node1: Node, node2: Node, sideZone1: Zone = None, sideZone2: Zone = None):
        self.node1: Node = node1
        self.node2: Node = node2
        self.sideZone1: Zone = sideZone1
        self.sideZone2: Zone = sideZone2
        self.dir: Direction = dir

    def __str__(self):
        s: str = str()
        s += "Edge has nodes connected: "+self.node1.name+" and "+self.node2.name+"\n"
        s += "\t zones connected: "
        if self.sideZone1 is not None:
            s+=self.sideZone1.zType+", "
        if self.sideZone2 is not None:
            s+=self.sideZone2.zType
        return s


class Zone():
    def __init__(self, x: int, y: int, zType: str, ulNode:Node = None, urNode: Node = None, dlNode: Node = None, drNode: Node = None):
        self.x: int = x
        self.y: int = y
        self.zType: str = zType
        #Upper Left Node
        self.ulNode: Node = ulNode
        #Upper Right Node
        self.urNode: Node = urNode
        #Down Right Node
        self.drNode: Node = drNode
        #Down Left Node
        self.dlNode: Node = dlNode

class Map:
    # q = quarentine place, v = vaccinated place, p = playground, e = empty
    def __init__(self, rows: int = 3, columns: int = 4, gridData =  [['q', 'v', 'p', 'e'],['v', 'e', 'q', 'e'], ['p', 'q', 'v', 'v']]):
        self.rows: int = rows
        self.columns: int = columns
        # Zones will be converted into a numpy 2d array of Zones
        self.zones = list(list())
        # A data member containing all of the edges
        self.edgeList: list[Edge] = list()

        # Generate the zones grid
        for i in range(len(gridData)):
            self.zones.append(list())
            for j in range(len(gridData[i])):
                self.zones[i].append(Zone(j, i, gridData[i][j]))
            self.zones[i] = np.array(self.zones[i])
        self.zones = np.array(self.zones)

        # Generate the Nodes
        x = 65
        nodes = list(list())
        for i in range(self.rows+1):
            nodes.append(list())
            for j in range(self.columns+1):
                nodes[i].append(Node(chr(x), j, i))
                x+=1

        # Setting each node corresponding to the zone
        zone: Zone
        for i in range(self.rows):
            for j in range(self.columns):
                zone = self.zones[i][j]
                zone.ulNode = nodes[i][j]
                zone.urNode = nodes[i][j+1]
                zone.dlNode = nodes[i+1][j]
                zone.drNode = nodes[i+1][j+1]
                if j == 0:
                    self.edgeList.append(Edge(nodes[i][j], nodes[i+1][j], None, self.zones[i][j]))
                else:
                    self.edgeList.append(Edge(nodes[i][j], nodes[i+1][j], self.zones[i][j-1], self.zones[i][j]))
                if i == 0:
                    self.edgeList.append(Edge(nodes[i][j], nodes[i][j+1], None, self.zones[i][j]))
                else:
                    self.edgeList.append(Edge(nodes[i][j], nodes[i][j+1], self.zones[i-1][j], self.zones[i][j]))
            self.edgeList.append(Edge(nodes[i][self.columns], nodes[i+1][self.columns], self.zones[i][self.columns-1], None))
        for j in range(self.columns):
            self.edgeList.append(Edge(nodes[self.rows][j], nodes[self.rows][j+1], self.zones[self.rows-1][j], None))

        # Now setting the node lists, unoptimal method and will improve later
        e: Edge
        n: Node
        nOther: Node
        for nodeList in nodes:
            for n in nodeList:
                for e in self.edgeList:
                    if n == e.node1 or n == e.node2:
                        n.edges.append(e)
                        if n == e.node1:
                            nOther = e.node2
                        elif n == e.node2:
                            nOther = e.node1
                        if nOther.x-n.x == 1:
                            n.rEdge = e
                        elif nOther.x-n.x == -1:
                            n.lEdge = e
                        elif nOther.y-n.y == 1:
                            n.dEdge = e
                        elif nOther.y-n.y == -1:
                            n.uEdge = e

    def __str__(self):
        s:str = str()




def printMap(map:Map):
    edge: Edge
    z: Zone
    e: Edge
    n: Node
    for i in range(len(map.zones)):
        for j in range(len(map.zones[i])):
            z = map.zones[i][j]
            print("Zone "+str(z.x)+","+str(z.y))
            print("Upper left node: "+z.ulNode.name+" has edges: ")
            for e in z.ulNode.edges:
                print(e)
            print("\nUpper Right node: "+z.urNode.name+" has edges: ")
            for e in z.urNode.edges:
                print(e)
            print("\nDown left node: "+z.dlNode.name+" has edges: ")
            for e in z.dlNode.edges:
                print(e)
            print("\nDown Right node: "+z.drNode.name+" has edges: ")
            for e in z.drNode.edges:
                print(e)
            print("*************************NEXT ZONE****************************")

