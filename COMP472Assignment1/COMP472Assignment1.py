from MapModule import *
import numpy as np
import math

class AStarAlgorithm():
    def __init__(self):
        self.openList: list[Node] = list()
        self.closedList: list[Node] = list()

class VaccinatedAStarAlgorithm(AStarAlgorithm):
    def getCostCardinal(self, edge: Edge):
        cost = float(0)
        switch = {
            'q': 3,
            'v': 0,
            'p': 1,
            'e': 2}
        z1 = edge.sideZone1
        z2 = edge.sideZone2
        if z1 is not None and z2 is not None:
            cost = 0.5*(switch.get(z1.zType)+switch.get(z2.zType))
        elif z1 is None:
            cost = switch.get(z2.zType)
        else:
            cost = switch.get(z2.zType)
        return cost

    # e00 and e01 represent 1 path to the diagonal while e10 and e11 represent the alternative path
    def getDiagCost(self, e00: Edge, e01: Edge, e10: Edge, e11: Edge):
        cost1: float  = math.sqrt(self.getCostCardinal(e00)**2 + self.getCostCardinal(e01)**2)
        cost2: float = math.sqrt(self.getCostCardinal(e10)**2 + self.getCostCardinal(e11)**2)
        return max(cost1, cost2)




def main():
    map = Map()
    v = VaccinatedAStarAlgorithm()
    z: Zone = map.zones[0][1]
    print("A->B Cost:" + str(v.getCostCardinal(map.zones[0][0].ulNode.rEdge)))
    print("B->C Cost:" + str(v.getCostCardinal(map.zones[0][1].ulNode.rEdge)))
    print("C->D Cost:" + str(v.getCostCardinal(map.zones[0][2].ulNode.rEdge)))
    print("D->E Cost:" + str(v.getCostCardinal(map.zones[0][3].ulNode.rEdge)))

    print("B->G Cost:" + str(v.getCostCardinal(map.zones[0][1].ulNode.dEdge)))
    print("C->H Cost:" + str(v.getCostCardinal(map.zones[0][2].ulNode.dEdge)))

    print("C->G Cost: "+str(v.getDiagCost(z.urNode.dEdge, z.drNode.lEdge, z.urNode.lEdge, z.ulNode.dEdge)))

main()