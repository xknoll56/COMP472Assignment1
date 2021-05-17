import numpy as np

class Node():
    pass
class Edge():
    pass
class Zone():
    pass

class Node():
    def __init__(self, name: str):
        self.name = name
        self.edges: list[Edge] = list()

class Edge():
    def __init__(self, node1: Node, node2: Node, sideZone1: Zone = None, sideZone2: Zone = None):
        self.node1 = node1
        self.node2 = node2
        self.sideZone1 = sideZone1
        self.sideZone2 = sideZone2

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
    def __init__(self, x: int, y: int, zType: str):
        self.x = x
        self.y = y
        self.zType = zType
        self.ulNode: Node = None
        self.urNode: Node = None
        self.drNode: Node = None
        self.dlNode: Node = None

class Map:
    # q = quarentine place, v = vaccinated place, p = playground, e = empty
    def __init__(self, rows: int = 3, columns: int = 4, gridData =  [['q', 'v', 'p', 'e'],['v', 'e', 'q', 'e'], ['p', 'q', 'v', 'v']]):
        self.rows = rows
        self.columns = columns
        self.zones = list(list())
        self.edgeList: list[Edge] = list()

        # Generate the zones grid
        for i in range(len(gridData)):
            self.zones.append(list())
            for j in range(len(gridData[i])):
                self.zones[i].append(Zone(j, i, gridData[i][j]))

        # Generate the Nodes
        x = 65
        nodes = list(list())
        for i in range(self.rows+1):
            nodes.append(list())
            for j in range(self.columns+1):
                nodes[i].append(Node(chr(x)))
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
                    edge = Edge(nodes[i][j], nodes[i+1][j], None, self.zones[i][j])
                    self.edgeList.append(edge)
                else:
                    edge = Edge(nodes[i][j], nodes[i+1][j], self.zones[i][j-1], self.zones[i][j])
                    self.edgeList.append(edge)
                if i == 0:
                    edge = Edge(nodes[i][j], nodes[i][j+1], None, self.zones[i][j])
                    self.edgeList.append(edge)
                else:
                    edge = Edge(nodes[i][j], nodes[i][j+1], self.zones[i-1][j], self.zones[i][j])
                    self.edgeList.append(edge)
            edge = Edge(nodes[i][self.columns], nodes[i+1][self.columns], self.zones[i][self.columns-1], None)
            self.edgeList.append(edge)
        for j in range(self.columns):
            edge = Edge(nodes[self.rows][j], nodes[self.rows][j+1], self.zones[self.rows-1][j], None)
            self.edgeList.append(edge)

        # Now setting the node lists, unoptimal method and will improve later
        e: Edge
        n: Node
        for nodeList in nodes:
            for n in nodeList:
                for e in self.edgeList:
                    if n == e.node1 or n == e.node2:
                        n.edges.append(e)


def main():
    edge: Edge
    map = Map()
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
            print("Upper Right node: "+z.urNode.name+" has edges: ")
            for e in z.urNode.edges:
                print(e)
            print("Down left node: "+z.dlNode.name+" has edges: ")
            for e in z.dlNode.edges:
                print(e)
            print("Down Right node: "+z.drNode.name+" has edges: ")
            for e in z.drNode.edges:
                print(e)
            print("*************************NEXT ZONE****************************")



main()