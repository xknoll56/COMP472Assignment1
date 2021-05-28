from Role import *

class RoleP(Role):

    def __init__(self, map: Map):
        cost_switch = {
            'q': float('inf'),
            'v': 2,
            'p': 0,
            'e': 1}
        super().__init__(map, cost_switch)


    def generate_path(self, start_zone: Zone, end_zone: Zone):
        # TODO This code is placeholder
        self.path.append(start_zone.upper_left_node)
        self.path.append(end_zone.upper_left_node)
        self.path[1].prevNode = self.path[0]

    # finds the cost of the Best-First Search solution path directly towards target.
    def best_first_search(self, orig: Node, targ: Node):
        print("---")
        # the cost of the lowest cost direct transition towards target.
        cost = float("inf")
        # the node with the lowest cost of the lowest cost direct transition towards target.
        best = None
        # distance to goal horizontally
        dx = targ.x - orig.x
        # distance to goal vertically
        dy = targ.y - orig.y
        print("dx=" + str(dx) + ", dy=" + str(dy))
        if dx > 0:  # the target is to the right of the current node
            print("target is to the right")
            edge_cost = self.get_cost_cardinal(orig.right_edge)
            print("the edge's cost is: " + str(edge_cost))
            if edge_cost < cost:  # this transition is more cost effective than current best.
                cost = edge_cost
                best = orig.right_node

        if dx < 0:  # the target is to the left of the current node
            print("target is to the left")
            edge_cost = self.get_cost_cardinal(orig.left_edge)
            print("the edge's cost is: " + str(edge_cost))
            if edge_cost < cost:  # this transition is more cost effective than current best.
                cost = edge_cost
                best = orig.left_node

        if dy > 0:  # the target is to the bottom of the current node
            print("target is to the bottom")
            edge_cost = self.get_cost_cardinal(orig.down_edge)
            print("the edge's cost is: " + str(edge_cost))
            if edge_cost < cost:  # this transition is more cost effective than current best.
                cost = edge_cost
                best = orig.lower_node

        if dy < 0:  # the target is to the top of the current node
            print("target is to the top")
            edge_cost = self.get_cost_cardinal(orig.up_edge)
            print("the edge's cost is: " + str(edge_cost))
            if edge_cost < cost:  # this transition is more cost effective than current best.
                cost = edge_cost
                best = orig.upper_node

        if cost == float("inf"):
            return cost
        if best is None:
            return 0  # origin is target
        else:
            return cost + self.best_first_search(best, targ)

    def get_heuristic(self, start: Node, targ: Node):
        # the total cost of traversing the Best-First Search solution path directly towards target.
        print("Initiating heuristic function for Role P with nodes: (" + str(start.x) + ", " + str(start.y) + "), (" + str(targ.x) + ", " + str(targ.y) + ")")
        return self.best_first_search(start, targ)


