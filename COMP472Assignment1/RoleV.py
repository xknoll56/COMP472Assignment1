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
        cur.f_value = self.get_heuristic_estimate(cur, targ)
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
                if tentative_g < diag.node.g_value:
                    n.prevNode = cur
                    n.g_value = tentative_g
                    n.f_value = n.g_value+self.get_heuristic_estimate(n, targ)
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
                    n.f_value = n.g_value+self.get_heuristic_estimate(n, targ)
                    if n not in self.openList:
                        self.priority_queue_push(n, n.f_value)

        #the path is constructed by starting at the goal and appending all the previious nodes until the start node is added
        self.path = []
        self.path.insert(0, cur)
        while cur != start:
            cur = cur.prevNode
            self.path.insert(0, cur)

    def get_heuristic_estimate(self, cur_node: Node, targ_node: Node):
        temp_node = cur_node
        cost: float = 0.0
        #loop while the temp node is not the target
        while temp_node != targ_node:
            #distance to goal horizontally
            dx = targ_node.x-temp_node.x
            #distance to goal vertically
            dy = targ_node.y-temp_node.y

            #If the goal is vertically algined, move only vertically
            if dx == 0:
                if dy > 0:
                    cost += self.get_cost_cardinal(temp_node.down_edge)
                    temp_node = temp_node.lower_node
                elif dy < 0:
                    cost += self.get_cost_cardinal(temp_node.up_edge)
                    temp_node = temp_node.upper_node
            #If the goal is horizontally alligned, move only horizontally
            elif dy == 0:
                if dx > 0:
                    cost += self.get_cost_cardinal(temp_node.right_edge)
                    temp_node = temp_node.right_node
                elif dx<0:
                    cost += self.get_cost_cardinal(temp_node.left_edge)
                    temp_node = temp_node.left_node
            #Otherwise move diagonally until its horizontally/vertically alligned
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




    def get_diag_cost(self, diag: Node.DiagonalConnection):
        cost1 : float = math.sqrt(self.get_cost_cardinal(diag.e00) ** 2 + self.get_cost_cardinal(diag.e01) ** 2)
        cost2 : float = math.sqrt(self.get_cost_cardinal(diag.e10) ** 2 + self.get_cost_cardinal(diag.e11) ** 2)
        return max(cost1, cost2)


