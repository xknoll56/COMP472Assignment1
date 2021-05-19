from MapModule import *
import numpy as np
import math

class AStarAlgorithm():
    def __init__(self):
        self.openList: list[Node] = list()
        self.closedList: list[Node] = list()

class VaccinatedAStarAlgorithm(AStarAlgorithm):
    def get_cost_cardinal(self, edge: Edge):
        cost = float(0)
        switch = {
            'q': 3,
            'v': 0,
            'p': 1,
            'e': 2}
        z1 = edge.side_zone_1
        z2 = edge.side_zone_2
        if z1 is not None and z2 is not None:
            cost = 0.5*(switch.get(z1.zone_type)+switch.get(z2.zone_type))
        elif z1 is None:
            cost = switch.get(z2.zone_type)
        else:
            cost = switch.get(z2.zone_type)
        return cost

    # e00 and e01 represent 1 path to the diagonal while e10 and e11 represent the alternative path
    def get_diag_cost(self, e00: Edge, e01: Edge, e10: Edge, e11: Edge):
        cost1: float  = math.sqrt(self.get_cost_cardinal(e00)**2 + self.get_cost_cardinal(e01)**2)
        cost2: float = math.sqrt(self.get_cost_cardinal(e10)**2 + self.get_cost_cardinal(e11)**2)
        return max(cost1, cost2)

class Test():
    def __init__(self, i):
        self.i = i

def main():
    map = Map()
    v = VaccinatedAStarAlgorithm()
    z: Zone = map.zones[0][1]
    print("A->B Cost:" + str(v.get_cost_cardinal(map.zones[0][0].upper_left_node.right_edge)))
    print("B->C Cost:" + str(v.get_cost_cardinal(map.zones[0][1].upper_left_node.right_edge)))
    print("C->D Cost:" + str(v.get_cost_cardinal(map.zones[0][2].upper_left_node.right_edge)))
    print("D->E Cost:" + str(v.get_cost_cardinal(map.zones[0][3].upper_left_node.right_edge)))

    print("B->G Cost:" + str(v.get_cost_cardinal(map.zones[0][1].upper_left_node.down_edge)))
    print("C->H Cost:" + str(v.get_cost_cardinal(map.zones[0][2].upper_left_node.down_edge)))

    print("C->G Cost: "+str(v.get_diag_cost(z.upper_right_node.down_edge, z.down_right_node.left_edge, z.upper_right_node.left_edge, z.upper_left_node.down_edge)))
  

main()