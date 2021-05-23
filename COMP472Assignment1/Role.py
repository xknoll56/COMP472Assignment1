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

    def generate_path(self, start_zone: Zone, end_zone: Zone):
        pass

    def priority_queue_push(self, node: Node, f_value):
        self.counter += 1
        heapq.heappush(self.openList, [f_value, self.counter, node])

    def priority_queue_pop(self):
        [f_value, counter, node] = heapq.heappop(self.openList)
        return node

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
