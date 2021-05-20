from MapModule import *
import math
import heapq

   

class AStarAlgorithm():
    def __init__(self, map: Map = Map()):
        #open list 
        self.openList : list[Node] = list()
        #the generated optimal path
        self.path: list[Node] = list()
        self.map = map
        self.counter = 0

    def generate_path(self):
        pass
    def priority_queue_push(self, node: Node, f_value):
        self.counter += 1
        heapq.heappush(self.openList, [f_value, self.counter, node])
    def priority_quene_pop(self):
        [f_value, counter, node] = heapq.heappop(self.openList)
        print("Poping "+node.name+" f_value: "+str(f_value))
        return node



class VaccinatedAStarAlgorithm(AStarAlgorithm):

    def generate_path(self, start_node: Node, end_node: Node):
        start: Node = start_node
        cur: Node = start
        targ: Node = end_node
        cur.g_value = 0.0
        cur.f_value = self.get_heuristic_estimate(cur, targ)
        self.priority_queue_push(cur, cur.f_value)
        while len(self.openList)>0:
            cur = self.priority_quene_pop()

            if cur == targ:
                print("Found target")
                break

            diag: Node.DiagonalConnection 
            for diag in cur.diags.values():
                n:Node = diag.node
                tentative_g = self.get_diag_cost(diag)+cur.g_value
                if tentative_g < diag.node.g_value:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value+self.get_heuristic_estimate(n, targ)
                    if n not in self.openList:
                        self.priority_queue_push(n, n.f_value)

                
            card: Node.CardinalConnection
            for card in cur.cardinals.values():
                n:Node = card.node
                tentative_g = self.get_cost_cardinal(card.edge)+cur.g_value
                if tentative_g < n.g_value:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value+self.get_heuristic_estimate(n, targ)
                    if n not in self.openList:
                        self.priority_queue_push(n, n.f_value)

        self.path = []
        self.path.insert(0, cur)
        while cur != start:
            cur = cur.prevNode
            self.path.insert(0, cur)

    def get_heuristic_estimate(self, cur_node: Node, targ_node: Node):
        temp_node = cur_node
        cost: float = 0.0
        while temp_node != targ_node:
            dx = targ_node.x-temp_node.x
            dy = targ_node.y-temp_node.y
            if dx == 0:
                if dy > 0:
                    cost += self.get_cost_cardinal(temp_node.down_edge)
                    temp_node = temp_node.lower_node
                elif dy < 0:
                    cost += self.get_cost_cardinal(temp_node.up_edge)
                    temp_node = temp_node.upper_node
            elif dy == 0:
                if dx > 0:
                    cost += self.get_cost_cardinal(temp_node.right_edge)
                    temp_node = temp_node.right_node
                elif dx<0:
                    cost += self.get_cost_cardinal(temp_node.left_edge)
                    temp_node = temp_node.left_node
            elif dx > 0 and dy > 0:
                cost += self.get_diag_cost(temp_node.diags[Diagonal.DOWN_RIGHT])
                temp_node = temp_node.lower_right_node
            elif dx < 0 and dy > 0:
                cost += self.get_diag_cost(temp_node.diags[Diagonal.DOWN_LEFT])
                temp_node = temp_node.lower_left_node
            elif dx < 0 and dy < 0:
                cost += self.get_diag_cost(temp_node.diags[Diagonal.UP_LEFT])
                temp_node = temp_node.upper_left_node
            elif dx >0 and dy <0:
                cost += self.get_diag_cost(temp_node.diags[Diagonal.UP_RIGHT])
                temp_node = temp_node.upper_right_node
        return cost




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
            cost = 0.5 * (switch.get(z1.zone_type) + switch.get(z2.zone_type))
        elif z1 is None:
            cost = switch.get(z2.zone_type)
        else:
            cost = switch.get(z1.zone_type)
        return cost


    def get_diag_cost(self, diag: Node.DiagonalConnection):
        cost1 : float = math.sqrt(self.get_cost_cardinal(diag.e00) ** 2 + self.get_cost_cardinal(diag.e01) ** 2)
        cost2 : float = math.sqrt(self.get_cost_cardinal(diag.e10) ** 2 + self.get_cost_cardinal(diag.e11) ** 2)
        return max(cost1, cost2)


def main():
    #map = Map.generate_random_map(15, 20)
    map = Map()
    v = VaccinatedAStarAlgorithm(map)
    bot_left: Zone = map.zones[map.rows-1][0]
    top_right: Zone = map.zones[0][map.columns-1]
    v.generate_path(bot_left.down_left_node, top_right.upper_right_node)
    node: Node
    for node in v.path:
        print(node.name)

  

main()



