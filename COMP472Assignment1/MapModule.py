import numpy as np
from enum import Enum

class Node():
    pass
class Edge():
    pass
class Zone():
    pass

class Diagonal(Enum):
    UP_RIGHT = 0
    DOWN_RIGHT = 1
    DOWN_LEFT = 2
    UP_LEFT = 3

class Node():
    def __init__(self, name: str, x:int, y:int):
        self.name: str = name
        self.x = x
        self.y = y
        #A list of all cardinal edges
        self.edges: list[Edge] = list()
        #Edge to the Right
        self.right_edge: Edge = None
        #Edge to Downward
        self.down_edge: Edge = None
        #Edge to the Left
        self.left_edge: Edge = None
        #Edge to Upward
        self.up_edge: Edge = None
        self.prevNode: Node = None

class Edge():
    def __init__(self, node1: Node, node2: Node, side_zone_1: Zone = None, side_zone_2: Zone = None):
        self.node1: Node = node1
        self.node2: Node = node2
        self.side_zone_1: Zone = side_zone_1
        self.side_zone_2: Zone = side_zone_2
        self.dir: Direction = dir

    def __str__(self):
        s: str = str()
        s += "Edge has nodes connected: "+self.node1.name+" and "+self.node2.name+"\n"
        s += "\t zones connected: "
        if self.side_zone_1 is not None:
            s+=self.side_zone_1.zone_type+", "
        if self.side_zone_2 is not None:
            s+=self.side_zone_2.zone_type
        return s


class Zone():
    def __init__(self, x: int, y: int, zone_type: str, upper_left_node:Node = None, upper_right_node: Node = None, down_left_node: Node = None, down_right_node: Node = None):
        self.x: int = x
        self.y: int = y
        self.zone_type: str = zone_type
        #Upper Left Node
        self.upper_left_node: Node = upper_left_node
        #Upper Right Node
        self.upper_right_node: Node = upper_right_node
        #Down Right Node
        self.down_right_node: Node = down_right_node
        #Down Left Node
        self.down_left_node: Node = down_left_node

class Map:
    # q = quarentine place, v = vaccinated place, p = playground, e = empty
    def __init__(self, rows: int = 3, columns: int = 4, grid_data =  [['q', 'v', 'p', 'e'],['v', 'e', 'q', 'e'], ['p', 'q', 'v', 'v']]):
        self.rows: int = rows
        self.columns: int = columns
        # Zones will be converted into a numpy 2d array of Zones
        self.zones = list(list())
        # A data member containing all of the edges
        self.edge_list: list[Edge] = list()

        # Generate the zones grid
        for i in range(len(grid_data)):
            self.zones.append(list())
            for j in range(len(grid_data[i])):
                self.zones[i].append(Zone(j, i, grid_data[i][j]))
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
                zone.upper_left_node = nodes[i][j]
                zone.upper_right_node = nodes[i][j+1]
                zone.down_left_node = nodes[i+1][j]
                zone.down_right_node = nodes[i+1][j+1]
                if j == 0:
                    self.edge_list.append(Edge(nodes[i][j], nodes[i+1][j], None, self.zones[i][j]))
                else:
                    self.edge_list.append(Edge(nodes[i][j], nodes[i+1][j], self.zones[i][j-1], self.zones[i][j]))
                if i == 0:
                    self.edge_list.append(Edge(nodes[i][j], nodes[i][j+1], None, self.zones[i][j]))
                else:
                    self.edge_list.append(Edge(nodes[i][j], nodes[i][j+1], self.zones[i-1][j], self.zones[i][j]))
            self.edge_list.append(Edge(nodes[i][self.columns], nodes[i+1][self.columns], self.zones[i][self.columns-1], None))
        for j in range(self.columns):
            self.edge_list.append(Edge(nodes[self.rows][j], nodes[self.rows][j+1], self.zones[self.rows-1][j], None))

        # Now setting the node lists, unoptimal method and will improve later
        e: Edge
        n: Node
        nOther: Node
        for nodeList in nodes:
            for n in nodeList:
                for e in self.edge_list:
                    if n == e.node1 or n == e.node2:
                        n.edges.append(e)
                        if n == e.node1:
                            nOther = e.node2
                        elif n == e.node2:
                            nOther = e.node1
                        if nOther.x-n.x == 1:
                            n.right_edge = e
                        elif nOther.x-n.x == -1:
                            n.left_edge = e
                        elif nOther.y-n.y == 1:
                            n.down_edge = e
                        elif nOther.y-n.y == -1:
                            n.up_edge = e

    def get_diag_zone(self, node: Node, diag: Diagonal):
        x = node.x
        y = node.y
        switcher1 = {
            Diagonal.DOWN_LEFT: -1,
            Diagonal.DOWN_RIGHT: 0,
            Diagonal.UP_LEFT: -1,
            Diagonal.UP_RIGHT: 0
            }
        x += switcher1.get(diag)
        switcher2 ={
            Diagonal.DOWN_LEFT: 0,
            Diagonal.DOWN_RIGHT: 0,
            Diagonal.UP_LEFT: -1,
            Diagonal.UP_RIGHT: -1
            }
        y += switcher2.get(diag)
        if y >= 0 and y<= self.rows and x >= 0 and x <= self.columns:
            return self.zones[y][x]
        else:
            return None

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
            print("Upper left node: "+z.upper_left_node.name+" has edges: ")
            for e in z.upper_left_node.edges:
                print(e)
            print("\nUpper Right node: "+z.upper_right_node.name+" has edges: ")
            for e in z.upper_right_node.edges:
                print(e)
            print("\nDown left node: "+z.down_left_node.name+" has edges: ")
            for e in z.down_left_node.edges:
                print(e)
            print("\nDown Right node: "+z.down_right_node.name+" has edges: ")
            for e in z.down_right_node.edges:
                print(e)
            print("*************************NEXT ZONE****************************")

