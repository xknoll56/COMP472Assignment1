# Role P is implemented by Jordan Goulet - 40075688

from Role import *

# Travels to the closest Playground.
class RoleP(Role):

    def __init__(self, map: Map):
        cost_switch = {
            'q': float('inf'),
            'v': 2,
            'p': 0,
            'e': 1}
        super().__init__(map, cost_switch)
        self.start = None  # The starting zone if any.
        self.end = None  # The end zone if any.
        self.first_edge = None  # The first edge traveled to from a starting zone if any.
        self.destinations: list[Node] = list()  # list of nodes that are possible destinations
        # Add all possible destination nodes to the list.
        for zone_arr in self.map.zones:
            for zone in zone_arr:
                if zone.zone_type == 'p':
                    if not zone.upper_left_node in self.destinations:
                        self.destinations.append(zone.upper_left_node)
                    if not zone.upper_right_node in self.destinations:
                        self.destinations.append(zone.upper_right_node)
                    if not zone.down_left_node in self.destinations:
                        self.destinations.append(zone.down_left_node)
                    if not zone.down_right_node in self.destinations:
                        self.destinations.append(zone.down_right_node)
        if len(self.destinations) < 1:
            print("The map does not have a playground, finding a path will be impossible.")

    def generate_path_closest(self, start):

        # If the starting point is a zone
        if isinstance(start, Zone):
            self.start = start

            # Check if a neighbor of the starting zone is a playground.
            # If so, the best path is straight to it.
            for zone in start.neighboring_zones:
                if zone.zone_type == "p":
                    self.end = zone
                    return

            # if no neighboring zones are playgrounds, then the path must move to an edge, then a node.
            # calculates the g and f values for each of the four corner nodes and pushes the nodes in the open list.
            top_edge = self.get_cost_cardinal(start.upper_left_node.right_edge)
            right_edge = self.get_cost_cardinal(start.down_right_node.up_edge)
            down_edge = self.get_cost_cardinal(start.down_right_node.left_edge)
            left_edge = self.get_cost_cardinal(start.upper_left_node.down_edge)
            node = start.upper_left_node
            node.g_value = min(left_edge, top_edge)
            node.f_value = node.g_value + self.get_heuristic(node)
            self.priority_queue_push(node, node.f_value)
            node = start.upper_right_node
            node.g_value = min(right_edge, top_edge)
            node.f_value = node.g_value + self.get_heuristic(node)
            self.priority_queue_push(node, node.f_value)
            node = start.down_left_node
            node.g_value = min(left_edge, down_edge)
            node.f_value = node.g_value + self.get_heuristic(node)
            self.priority_queue_push(node, node.f_value)
            node = start.down_right_node
            node.g_value = min(right_edge, down_edge)
            node.f_value = node.g_value + self.get_heuristic(node)
            self.priority_queue_push(node, node.f_value)

        # If the starting point is a node
        else:
            # calculate the g and f values of the start node and push it in the open list.
            start.g_value = 0.0
            start.f_value = self.get_heuristic(start)
            self.priority_queue_push(start, start.f_value)

        # Begin iterating through the open list.
        while len(self.openList) > 0:

            # take the current as the node with the lowest F value
            cur = self.priority_queue_pop()

            # if its heuristic is 0, we must be at a playground (the target), built the path.
            if self.get_heuristic(cur) <= 0:
                print("Found target")
                # the path is constructed by appending all the previous nodes until the start node.
                self.path = []
                self.path.insert(0, cur)
                while cur is not None:
                    cur = cur.prevNode
                    if cur is None:
                        break
                    else:
                        self.path.insert(0, cur)

                # if the path started in a zone, find which edge was travelled to first.
                if self.start is not None:
                    if start.upper_left_node == self.path[0]:
                        if left_edge > top_edge:
                            self.first_edge = left_edge
                        else:
                            self.first_edge = top_edge
                    elif start.upper_right_node == self.path[0]:
                        if right_edge > top_edge:
                            self.first_edge = right_edge
                        else:
                            self.first_edge = top_edge
                    elif start.down_left_node == self.path[0]:
                        if left_edge > down_edge:
                            self.first_edge = left_edge
                        else:
                            self.first_edge = down_edge
                    elif start.down_right_node == self.path[0]:
                        if right_edge > down_edge:
                            self.first_edge = right_edge
                        else:
                            self.first_edge = down_edge
                    else:
                        # this should be unreachable
                        print("ERROR. couldn't calculate the first edge.")
                return

            # iterate through the cardinals
            for card in cur.cardinals.values():
                n = card.node
                tentative_g = self.get_cost_cardinal(card.edge) + cur.g_value
                # if the new path leading to the node has a lower cost, this should become its g value.
                if tentative_g < n.g_value:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value + self.get_heuristic(n)
                    if n not in self.openList and n.q_limit > 0:
                        self.priority_queue_push(n, n.f_value)

        # The open list is empty, no path was found.
        print("No path is found. Please try again!")
        print("This means that there is no possible path from the starting point "
              "to a playground that does pass through an infinity cost edge.")

    # Calculates (if not already calculated previously) and returns the h value for the given node.
    # The heuristic value is the manhattan distance to the closest playground.
    # This heuristic is admissible because the manhatthan distance to the closest playground cannot be an over estimate
    # since that would mean one of the edges traveled has cost less than 1 and this in turn would mean that one of the
    # two zones adjacent to this edge is a playground, meaning that the original manhattan distance calculated was not
    # in fact the closest playground. Thus this heuristic function cannot be an over estimate of the actual cost.
    def get_heuristic(self, start):
        # The h value for this node hasnt been calculated yet, calculate it.
        if start.h_value is None:
            min_dist = float("inf")
            for node in self.destinations:
                dist = abs(node.x - start.x) + abs(node.y - start.y)
                if dist < min_dist:
                    min_dist = dist
            start.h_value = min_dist
        return start.h_value
