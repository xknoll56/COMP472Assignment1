from MapModule import *
import math
import heapq

   

class Role():
    def __init__(self, map: Map = Map(), cost_switch = {}):
        #open list 
        self.openList : list[Node] = list()
        #the generated optimal path
        self.path: list[Node] = list()
        self.map = map
        self.counter = 0
        self.cost_switch = cost_switch

        self.dir_switch = {
            (1,0): Cardinal.RIGHT,
            (1,1): Diagonal.DOWN_RIGHT,
            (0,1): Cardinal.DOWN,
            (-1,1): Diagonal.DOWN_LEFT,
            (-1,0):Cardinal.LEFT,
            (-1,-1):Diagonal.UP_LEFT,
            (0,-1):Cardinal.UP,
            (1,-1):Diagonal.UP_RIGHT}
        n: Node
        self.node_switch = {
            (1,0): lambda n : n.right_node,
            (1,1): lambda n : n.lower_right_node,
            (0,1): lambda n : n.lower_node,
            (-1,1): lambda n : n.lower_left_node,
            (-1,0): lambda n : n.left_node,
            (-1,-1): lambda n : n.upper_left_node,
            (0,-1): lambda n : n.upper_node,
            (1,-1): lambda n : n.upper_right_node}



    def generate_path(self, start_zone: Zone, end_zone: Zone):
        pass

    def priority_queue_push(self, node: Node, f_value):
        i: int = 0
        added: int = 0
        for next in self.openList:
            if f_value >= next[0]:
                self.openList.insert(i, (f_value, node))
                added = 1
                break
            i+=1
        if not added:
            self.openList.append((f_value, node))

    def priority_queue_pop(self):
        (f_value, node) = self.openList.pop()
        return node

    #def priority_queue_push(self, node: Node, f_value):
    #    self.counter += 1
    #    self.openList.append((f_value, self.counter, node))

    #def priority_queue_pop(self):
    #    self.openList.sort()
    #    (f_value, counter, node) = self.openList.pop(0)
    #    return node

    #def priority_queue_push(self, node: Node, f_value):
    #    self.counter += 1
    #    heapq.heappush(self.openList, [f_value, self.counter, node])

    #def priority_queue_pop(self):
    #    [f_value, counter, node] = heapq.heappop(self.openList)
    #    return node

    def get_cost_cardinal(self, edge: Edge):
        cost = float(0)
        z1 = edge.side_zone_1
        z2 = edge.side_zone_2

        if z1 is not None and z2 is not None:
            cost = 0.5 * (self.cost_switch.get(z1.zone_type) + self.cost_switch.get(z2.zone_type))
        elif z1 is None:
            cost = self.cost_switch.get(z2.zone_type)
        else:
            cost = self.cost_switch.get(z1.zone_type)
        return cost



    #def priority_queue_push(self, node: Node, f_value):
    #    self.counter += 1
    #    heapq.heappush(self.openList, [f_value, self.counter, node])

    #def priority_queue_pop(self):
    #    [f_value, counter, node] = heapq.heappop(self.openList)
    #    return node