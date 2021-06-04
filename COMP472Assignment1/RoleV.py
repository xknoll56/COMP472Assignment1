from Role import *



class RoleV(Role):

    def __init__(self, map: Map):
        cost_switch = {
            'q': 3,
            'v': 0,
            'p': 1,
            'e': 2}
        super().__init__(map, cost_switch)
        self.destinations: list[Node] = list()
        zone:Zone
        for zone_arr in self.map.zones:
            for zone in zone_arr:
                if zone.zone_type == 'v':
                    self.destinations.append(zone.down_left_node)

    def generate_path_closest(self, start_zone: Zone):

        #Establish the final and start nodes taken as the bottom left nodes of the entered zones
        start: Node = start_zone.down_left_node
        cur: Node = start
        zone: Zone


        #caclulate the heuristic values of the start node
        cur.g_value = 0.0
        cur.f_value = self.get_closest_heuristic(cur)
        self.priority_queue_push(cur, cur.f_value)

        #Begin iterating throught he openlist
        while len(self.openList)>0:

            #take the current as the node with the lowest F value
            cur = self.priority_queue_pop()

            #if the current is the target then the algorithm is complete
            if self.get_closest_heuristic(cur) == 0 and self.map.get_diag_zone(cur, Diagonal.UP_RIGHT).zone_type == 'v':
                print("Found target")
                break
            

            #iterate through the diagonals 
            diag: Node.DiagonalConnection 
            for diag in cur.diags.values():
                n:Node = diag.node
                tentative_g = self.get_diag_cost(diag)+cur.g_value
                #if tentative g score is less then the current g score then reparent the node and recalculate its 
                #g and f scores, if its not on the open list add it
                if tentative_g < diag.node.g_value and n.q_limit>0:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value+self.get_closest_heuristic(n)
                    if n not in self.openList:
                        self.priority_queue_push(n, n.f_value)

            #iterate through the cardinals 
            card: Node.CardinalConnection
            for card in cur.cardinals.values():
                n:Node = card.node
                tentative_g = self.get_cost_cardinal(card.edge)+cur.g_value
                if tentative_g < n.g_value:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value+self.get_closest_heuristic(n)
                    if n not in self.openList and n.q_limit>0:
                        self.priority_queue_push(n, n.f_value)

        #the path is constructed by starting at the goal and appending all the previious nodes until the start node is added
        self.path = []
        self.path.insert(0, cur)
        while cur != start:
            cur = cur.prevNode
            self.path.insert(0, cur)




    def get_closest_heuristic(self, start: Node):
        root_2 = math.sqrt(2)
        closest_dest: Node
        min_dist: float = self.map.columns+self.map.rows+2
        node: Node
        min_dx: int
        min_dy: int
        for node in self.destinations:
            #distance to node horizontally
            dx = node.x-start.x
            #distance to node vertically
            dy = node.y-start.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < min_dist:
                min_dx = dx
                min_dy = dy
                min_dist = dist
                closest_dest = node
        heuristic: float
        if min_dx < 0 and min_dy > 0:
            diag: Node.DiagonalConnection = closest_dest.diags[Diagonal.UP_RIGHT]
            amount_saved_diag: float = max(root_2 - self.get_diag_cost(diag), 0)
            if (-1*min_dx) > min_dy:
                amount_saved_hor: float = max(1 - self.get_cost_cardinal(closest_dest.right_edge), 0)
                amount_saved: float = max(amount_saved_diag, amount_saved_hor)
                heuristic = (min_dy+min_dx)+(min_dy)*root_2-amount_saved
            else:
                amount_saved_vert: float = max(1 - self.get_cost_cardinal(closest_dest.up_edge), 0)
                amount_saved: float = max(amount_saved_diag, amount_saved_vert)
                heuristic = (min_dx+min_dy)+(-1*min_dx)*root_2-amount_saved
        elif min_dx < 0 and min_dy < 0:
            if min_dx < min_dy:
                amount_saved: float = max(1 - self.get_cost_cardinal(closest_dest.right_edge), 0)
                heuristic = (min_dy-min_dx) + (-1*min_dy)*root_2-amount_saved
            else:
                heuristic = (min_dx-min_dy) + (-1*min_dx)*root_2
        elif min_dx > 0 and min_dy > 0:
            if min_dy > min_dy:
                amount_saved: float = max(1 - self.get_cost_cardinal(closest_dest.up_edge), 0)
                heuristic = (min_dy-min_dx)+min_dx*root_2-amount_saved
            else:
                heuristic = (min_dx-min_dy)+min_dy*root_2
        elif min_dx > 0 and min_dy < 0:
            max_dir = max(min_dx, -1*min_dy)
            min_dir = min(min_dx, -1*min_dy)
            heuristic = (max_dir-min_dir)+min_dir*root_2
        else:
            if min_dx == 0:
                heuristic = abs(min_dy)
            else:
                heuristic = abs(min_dx)

        return heuristic



    def generate_path(self, start_zone: Zone, end_zone: Zone):

        #Establish the final and start nodes taken as the bottom left nodes of the entered zones
        start: Node = start_zone.down_left_node
        cur: Node = start
        targ: Node = end_zone.down_left_node

        #caclulate the heuristic values of the start node
        cur.g_value = 0.0
        cur.f_value = self.get_heuristic(cur, targ)
        self.priority_queue_push(cur, cur.f_value)

        #Begin iterating throught he openlist
        while len(self.openList)>0:

            #take the current as the node with the lowest F value
            cur = self.priority_queue_pop()

            #if the current is the target then the algorithm is complete
            if cur == targ:
                print("Found target")
                break
            

            #iterate through the diagonals 
            diag: Node.DiagonalConnection 
            for diag in cur.diags.values():
                n:Node = diag.node
                tentative_g = self.get_diag_cost(diag)+cur.g_value
                #if tentative g score is less then the current g score then reparent the node and recalculate its 
                #g and f scores, if its not on the open list add it
                if tentative_g < diag.node.g_value and n.q_limit>0:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value+self.get_heuristic(n, targ)
                    if n not in self.openList:
                        self.priority_queue_push(n, n.f_value)

            #iterate through the cardinals 
            card: Node.CardinalConnection
            for card in cur.cardinals.values():
                n:Node = card.node
                tentative_g = self.get_cost_cardinal(card.edge)+cur.g_value
                if tentative_g < n.g_value:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value+self.get_heuristic(n, targ)
                    if n not in self.openList and n.q_limit>0:
                        self.priority_queue_push(n, n.f_value)

        #the path is constructed by starting at the goal and appending all the previious nodes until the start node is added
        self.path = []
        self.path.insert(0, cur)
        while cur != start:
            cur = cur.prevNode
            self.path.insert(0, cur)

    def get_heuristic(self, start: Node, targ: Node):
        head: Node = start
        head2: Node = start
        cost: float = self.get_heuristic_direct(start, targ)
        #distance to goal horizontally
        dx = targ.x-start.x
        #distance to goal vertically
        dy = targ.y-start.y

        if abs(dy) > 4:
            for i in range(abs(dy)):
                cost = min(cost, self.get_heuristic_direct(start, head)+self.get_heuristic_direct(head, targ))
                if dy > 0:
                    head = head.lower_node
                else:
                    head = head.upper_node
        else:
            for i in range(abs(4)):
                cost = min(cost, self.get_heuristic_direct(start, head)+self.get_heuristic_direct(head, targ))
                cost = min(cost, self.get_heuristic_direct(start, head2)+self.get_heuristic_direct(head2, targ))
                if head.has_lower_edge():
                    head = head.lower_node
                if head2.has_upper_edge():
                    head2 = head2.upper_node

        if abs(dx) > 4:
            head = start
            for i in range(abs(dx)):
                cost = min(cost, self.get_heuristic_direct(start, head) + self.get_heuristic_direct(head, targ))
                if dx > 0:
                    head = head.right_node
                else:
                    head = head.left_node
        else:
            head = start
            head2 = start
            for i in range(4):
                cost = min(cost, self.get_heuristic_direct(start, head)+self.get_heuristic_direct(head, targ))
                cost = min(cost, self.get_heuristic_direct(start, head2)+self.get_heuristic_direct(head2, targ))
                if head.has_right_edge():
                    head = head.right_node
                if head2.has_left_edge():
                    head2 = head2.left_node


        return cost



    def get_heuristic_direct(self, cur_node: Node, targ_node: Node):
        temp_node = cur_node
        cost: float = 0.0
        #loop while the temp node is not the target
        while temp_node != targ_node:
            #distance to goal horizontally
            dx = targ_node.x-temp_node.x
            #distance to goal vertically
            dy = targ_node.y-temp_node.y

            #normalize the direction
            v: list[int] = [dx, dy]
            if abs(dx) > 0:
                v[0] = int(v[0]/abs(v[0]))
            if abs(dy) > 0:
                v[1] = int(v[1]/abs(v[1]))

            v = tuple(v)
            dir = self.dir_switch.get(v)

            if isinstance(dir, Cardinal):
                card: Node.CardinalConnection = temp_node.cardinals[dir]
                cost += self.get_cost_cardinal(card.edge)
                temp_node = self.node_switch.get(v)(temp_node)
            elif isinstance(dir, Diagonal):
                diag: Node.DiagonalConnection = temp_node.diags[dir]
                cost += self.get_diag_cost(diag)
                temp_node = self.node_switch.get(v)(temp_node)

        return cost




    def get_diag_cost(self, diag: Node.DiagonalConnection):
        cost1 : float = math.sqrt(self.get_cost_cardinal(diag.e00) ** 2 + self.get_cost_cardinal(diag.e01) ** 2)
        cost2 : float = math.sqrt(self.get_cost_cardinal(diag.e10) ** 2 + self.get_cost_cardinal(diag.e11) ** 2)
        return max(cost1, cost2)


