# ----------------------------------------------------------------------------------------------------
#	RoleV Algorithm Class
#	Author: Xavier Knoll (40132134)
# ----------------------------------------------------------------------------------------------------
from Role import *



class RoleV(Role):

    def __init__(self, map: Map):
        cost_switch = {
            'q': 3,
            'v': 0,
            'p': 1,
            'e': 2}
        super().__init__(map, cost_switch)
        self.destinations : list[Node] = list()
        zone :Zone
        for zone_arr in self.map.zones:
            for zone in zone_arr:
                if zone.zone_type == 'v':
                    self.destinations.append(zone.down_left_node)

    #This method will generate the path based on the least cost (not the least
    #distance) to a goal using admissible heuristics
    def generate_path_closest(self, start_zone: Zone):

        #Establish the final and start nodes taken as the bottom left nodes of
        #the entered zones
        start : Node = start_zone.down_left_node
        cur : Node = start
        zone : Zone


        #caclulate the heuristic values of the start node
        cur.g_value = 0.0
        cur.f_value = self.get_closest_heuristic(cur)
        self.priority_queue_push(cur, cur.f_value)

        #Begin iterating throught he openlist
        while len(self.openList) > 0:

            #take the current as the node with the lowest F value
            cur = self.priority_queue_pop()

            #if the current is the target then the algorithm is complete
            if self.get_closest_heuristic(cur) == 0 and self.map.get_diag_zone(cur, Diagonal.UP_RIGHT).zone_type == 'v':
                print("Found target")
                self.path_cost = cur.g_value
                break
            

            #iterate through the diagonals
            diag : Node.DiagonalConnection 
            for diag in cur.diags.values():
                n :Node = diag.node
                tentative_g = self.get_diag_cost(diag) + cur.g_value
                #if tentative g score is less then the current g score then
                #reparent the node and recalculate its
                #g and f scores, if its not on the open list add it
                if tentative_g < diag.node.g_value and n.q_limit > 0:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value + self.get_closest_heuristic(n)
                    if n not in self.openList:
                        self.priority_queue_push(n, n.f_value)

            #iterate through the cardinals
            card : Node.CardinalConnection
            for card in cur.cardinals.values():
                n :Node = card.node
                tentative_g = self.get_cost_cardinal(card.edge) + cur.g_value
                if tentative_g < n.g_value:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value + self.get_closest_heuristic(n)
                    if n not in self.openList and n.q_limit > 0:
                        self.priority_queue_push(n, n.f_value)

        #the path is constructed by starting at the goal and appending all the
        #previious nodes until the start node is added
        self.path = []
        self.path.insert(0, cur)
        while cur != start:
            cur = cur.prevNode
            self.path.insert(0, cur)



    #The main heuristics method that will aquire the heuristic to the closest
    #destination while adhearing to admissiblity.  The basis of the algorithm
    #will calculate the cost by using the minimum possible movement cost for a
    #diagonal target to a goal, which is the square root of 2 for each
    #diagonal, plus the minimum vertical/horizontal movement cost towards a
    #goal, which is 1 for every movement, minus a correction factor for when
    #you must move through a goal zone to the nearest goal and the value may be
    #less then 1 or root 2 (that helps guarentee admissiblility)
    def get_closest_heuristic(self, start: Node):
        min_dist : float = self.map.columns + self.map.rows + 2
        node : Node
        #First the closest destination is found.
        for node in self.destinations:
            #distance to node horizontally
            dx = node.x - start.x
            #distance to node vertically
            dy = node.y - start.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < min_dist:
                min_dist = dist
        #On the rare chance there is multiple destinations at equal length,
        #there could be slightly different admissibilities due to the
        #correction factor so all must be checked.
        closests : list[tuple] = list()
        for node in self.destinations:
            #distance to node horizontally
            dx = node.x - start.x
            #distance to node vertically
            dy = node.y - start.y
            dist = math.sqrt(dx * dx + dy * dy)
            if math.isclose(dist, min_dist):
                closests.append((dx, dy, node))
        #Finally we'll take the minimum of all heuristics of the same distance
        heuristic : float = float('inf')
        for c in closests:
            heuristic = min(heuristic, self.admissiblity_correction(c[0], c[1], c[2]))
        return heuristic

    #In order for the destination to guarantee admissiblity, a correction mus
    #be made.  For instance, if the destination is on the bottom left corner of
    #the map, moving on the edge to the left toward the destination will be of
    #0 cost.  This means that any heuristic needs to check if it saves more
    #more moving through this edge and subtract the amount saved from the
    #original heuristic formulae.
    def admissiblity_correction(self, min_dx: int, min_dy: int, closest_dest: Node):
        root_2 = math.sqrt(2)
        heuristic : float
        #Case 1: the goal is to the down left of the current node.
        if min_dx < 0 and min_dy > 0:
            diag : Node.DiagonalConnection = closest_dest.diags[Diagonal.UP_RIGHT]
            #The amount saved is the same as a normal movement (root(2)) minus
            #the cost of the diagonal to a maximum of 0.
            amount_saved_diag : float = max(root_2 - self.get_diag_cost(diag), 0)
            #If the goal is more horizontally aligned, a check must be made to
            #see if running through the bottom edge saves more than through the
            #diagonal on the heuristic.
            if (-1 * min_dx) > min_dy:
                amount_saved_hor : float = max(1 - self.get_cost_cardinal(closest_dest.right_edge), 0)
                amount_saved : float = max(amount_saved_diag, amount_saved_hor)
                heuristic = (min_dy + min_dx) + (min_dy) * root_2 - amount_saved
            #Otherwise we must check the vertical edge to see if it saves more
            #and account for this.
            else:
                amount_saved_vert : float = max(1 - self.get_cost_cardinal(closest_dest.up_edge), 0)
                amount_saved : float = max(amount_saved_diag, amount_saved_vert)
                heuristic = (min_dx + min_dy) + (-1 * min_dx) * root_2 - amount_saved
        #Next Case is moving to the top right where we need to compare the
        #amount saved on the right edge on the destination.
        elif min_dx < 0 and min_dy < 0:
            if min_dx < min_dy:
                amount_saved : float = max(1 - self.get_cost_cardinal(closest_dest.right_edge), 0)
                heuristic = (min_dy - min_dx) + (-1 * min_dy) * root_2 - amount_saved
            else:
                heuristic = (min_dx - min_dy) + (-1 * min_dx) * root_2
        #Next moveing to the bottom left the upper edge needs to check for the
        #amount saved.
        elif min_dx > 0 and min_dy > 0:
            if min_dy > min_dy:
                amount_saved : float = max(1 - self.get_cost_cardinal(closest_dest.up_edge), 0)
                heuristic = (min_dy - min_dx) + min_dx * root_2 - amount_saved
            else:
                heuristic = (min_dx - min_dy) + min_dy * root_2
        #Moving to the top right no heurisic correction needs to be made
        #because you're guarenteed to not run through any goal zones.
        elif min_dx > 0 and min_dy < 0:
            max_dir = max(min_dx, -1 * min_dy)
            min_dir = min(min_dx, -1 * min_dy)
            heuristic = (max_dir - min_dir) + min_dir * root_2
        #If the goal is horizontally alligned
        else:
            if min_dx == 0 and min_dy != 0:
                if min_dy < 0:
                    heuristic = abs(min_dy)
                else:
                    #A correction must be made if moving down through the goal
                    #zone.
                    amount_saved : float = max(1 - self.get_cost_cardinal(closest_dest.up_edge), 0)
                    heuristic = min_dy - amount_saved
            elif min_dy == 0 and min_dx != 0:
                if min_dx > 0:
                    heuristic = min_dx
                else:
                    #A correction must be made if moving left through a goal
                    #zone.
                    amount_saved : float = max(1 - self.get_cost_cardinal(closest_dest.right_edge), 0)
                    heuristic = abs(min_dx) - amount_saved
            else:
                heuristic = 0
        return heuristic


    #These were functions made at first that calculate a path to a specific
    #zone, although not admissibly because that is not possible.
    def generate_path(self, start_zone: Zone, end_zone: Zone):

        #Establish the final and start nodes taken as the bottom left nodes of
        #the entered zones
        start : Node = start_zone.down_left_node
        cur : Node = start
        targ : Node = end_zone.down_left_node

        #caclulate the heuristic values of the start node
        cur.g_value = 0.0
        cur.f_value = self.get_heuristic(cur, targ)
        self.priority_queue_push(cur, cur.f_value)

        #Begin iterating throught he openlist
        while len(self.openList) > 0:

            #take the current as the node with the lowest F value
            cur = self.priority_queue_pop()

            #if the current is the target then the algorithm is complete
            if cur == targ:
                print("Found target")
                break
            

            #iterate through the diagonals
            diag : Node.DiagonalConnection 
            for diag in cur.diags.values():
                n :Node = diag.node
                tentative_g = self.get_diag_cost(diag) + cur.g_value
                #if tentative g score is less then the current g score then
                #reparent the node and recalculate its
                #g and f scores, if its not on the open list add it
                if tentative_g < diag.node.g_value and n.q_limit > 0:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value + self.get_heuristic(n, targ)
                    if n not in self.openList:
                        self.priority_queue_push(n, n.f_value)

            #iterate through the cardinals
            card : Node.CardinalConnection
            for card in cur.cardinals.values():
                n :Node = card.node
                tentative_g = self.get_cost_cardinal(card.edge) + cur.g_value
                if tentative_g < n.g_value:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value + self.get_heuristic(n, targ)
                    if n not in self.openList and n.q_limit > 0:
                        self.priority_queue_push(n, n.f_value)

        #the path is constructed by starting at the goal and appending all the
        #previious nodes until the start node is added
        self.path = []
        self.path.insert(0, cur)
        while cur != start:
            cur = cur.prevNode
            self.path.insert(0, cur)

    #Heuristic function that will calculate a non-admissible heuristic based on a target specified.
    def get_heuristic(self, start: Node, targ: Node):
        head : Node = start
        head2 : Node = start
        cost : float = self.get_cost_direct(start, targ)
        #distance to goal horizontally
        dx = targ.x - start.x
        #distance to goal vertically
        dy = targ.y - start.y

        if abs(dy) > 4:
            for i in range(abs(dy)):
                cost = min(cost, self.get_cost_direct(start, head) + self.get_cost_direct(head, targ))
                if dy > 0:
                    head = head.lower_node
                else:
                    head = head.upper_node
        else:
            for i in range(abs(4)):
                cost = min(cost, self.get_cost_direct(start, head) + self.get_cost_direct(head, targ))
                cost = min(cost, self.get_cost_direct(start, head2) + self.get_cost_direct(head2, targ))
                if head.has_lower_edge():
                    head = head.lower_node
                if head2.has_upper_edge():
                    head2 = head2.upper_node

        if abs(dx) > 4:
            head = start
            for i in range(abs(dx)):
                cost = min(cost, self.get_cost_direct(start, head) + self.get_cost_direct(head, targ))
                if dx > 0:
                    head = head.right_node
                else:
                    head = head.left_node
        else:
            head = start
            head2 = start
            for i in range(4):
                cost = min(cost, self.get_cost_direct(start, head) + self.get_cost_direct(head, targ))
                cost = min(cost, self.get_cost_direct(start, head2) + self.get_cost_direct(head2, targ))
                if head.has_right_edge():
                    head = head.right_node
                if head2.has_left_edge():
                    head2 = head2.left_node


        return cost



    def get_cost_direct(self, cur_node: Node, targ_node: Node):
        temp_node = cur_node
        cost : float = 0.0
        #loop while the temp node is not the target
        while temp_node != targ_node:
            #distance to goal horizontally
            dx = targ_node.x - temp_node.x
            #distance to goal vertically
            dy = targ_node.y - temp_node.y

            #normalize the direction
            v : list[int] = [dx, dy]
            if abs(dx) > 0:
                v[0] = int(v[0] / abs(v[0]))
            if abs(dy) > 0:
                v[1] = int(v[1] / abs(v[1]))

            v = tuple(v)
            dir = self.dir_switch.get(v)

            if isinstance(dir, Cardinal):
                card : Node.CardinalConnection = temp_node.cardinals[dir]
                cost += self.get_cost_cardinal(card.edge)
                temp_node = self.node_switch.get(v)(temp_node)
            elif isinstance(dir, Diagonal):
                diag : Node.DiagonalConnection = temp_node.diags[dir]
                cost += self.get_diag_cost(diag)
                temp_node = self.node_switch.get(v)(temp_node)

        return cost




    def get_diag_cost(self, diag: Node.DiagonalConnection):
        cost1 : float = math.sqrt(self.get_cost_cardinal(diag.e00) ** 2 + self.get_cost_cardinal(diag.e01) ** 2)
        cost2 : float = math.sqrt(self.get_cost_cardinal(diag.e10) ** 2 + self.get_cost_cardinal(diag.e11) ** 2)
        return max(cost1, cost2)


