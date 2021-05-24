from Role import *



class RoleV(Role):

    def __init__(self, map: Map):
        cost_switch = {
            'q': 3,
            'v': 0,
            'p': 1,
            'e': 2}
        super().__init__(map, cost_switch)

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
        cost: float = self.get_heuristic_direct(start, targ)
        #distance to goal horizontally
        dx = targ.x-start.x
        #distance to goal vertically
        dy = targ.y-start.y

        for i in range(abs(dy)):
            cost = min(cost, self.get_heuristic_direct(start, head)+self.get_heuristic_direct(head, targ))
            if dy > 0:
                head = head.lower_node
            else:
                head = head.upper_node
        head = start
        for i in range(abs(dx)):
            cost = min(cost, self.get_heuristic_direct(start, head) + self.get_heuristic_direct(head, targ))
            if dx > 0:
                head = head.right_node
            else:
                head = head.left_node

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

            if isinstance(dir, Diagonal):
                diag: Node.DiagonalConnection = temp_node.diags[dir]
                cost += self.get_diag_cost(diag)
                temp_node = self.node_switch.get(v)(temp_node)

        return cost




    def get_diag_cost(self, diag: Node.DiagonalConnection):
        cost1 : float = math.sqrt(self.get_cost_cardinal(diag.e00) ** 2 + self.get_cost_cardinal(diag.e01) ** 2)
        cost2 : float = math.sqrt(self.get_cost_cardinal(diag.e10) ** 2 + self.get_cost_cardinal(diag.e11) ** 2)
        return max(cost1, cost2)


