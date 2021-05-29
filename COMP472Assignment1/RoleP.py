from Role import *

class RoleP(Role):

    def __init__(self, map: Map):
        cost_switch = {
            'q': float('inf'),
            'v': 2,
            'p': 0,
            'e': 1}
        super().__init__(map, cost_switch)


    def generate_path(self, start, targ):

        cur: Node = start

        # caclulate the heuristic values of the start node
        cur.g_value = 0.0
        cur.f_value = self.get_heuristic(cur, targ)
        self.priority_queue_push(cur, cur.f_value)

        # Begin iterating throught he openlist
        while len(self.openList) > 0:

            # take the current as the node with the lowest F value
            cur = self.priority_queue_pop()

            # if the current is the target then the algorithm is complete
            if cur == targ:
                print("Found target")
                break

            # iterate through the cardinals
            for card in cur.cardinals.values():
                n: Node = card.node
                tentative_g = self.get_cost_cardinal(card.edge) + cur.g_value
                if tentative_g < n.g_value:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value + self.get_heuristic(n, targ)
                    if n not in self.openList and n.q_limit > 0:
                        self.priority_queue_push(n, n.f_value)

        if (cur != targ):
            # TODO no path possible
            print("There is no possible path from the starting point to the end point that does not travel along a quarantine zone.")

        # the path is constructed by starting at the goal and appending all the previious nodes until the start node is added
        self.path = []
        self.path.insert(0, cur)
        while cur != start:
            cur = cur.prevNode
            self.path.insert(0, cur)

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

    def get_heuristic(self, start, targ):
        # the total cost of traversing the Best-First Search solution path directly towards target.
        print("Initiating heuristic function for Role P with nodes: (" + str(start.x) + ", " + str(start.y) + "), (" + str(targ.x) + ", " + str(targ.y) + ")")
        return self.best_first_search(start, targ)


