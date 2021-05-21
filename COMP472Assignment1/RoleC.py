from Role import *

class RoleC(Role):

    def __init__(self, map: Map):
        cost_switch = {
            'q': 0,
            'v': 2,
            'p': 3,
            'e': 1}
        super().__init__(map, cost_switch)


    def generate_path(self, start_zone: Zone, end_zone: Zone):

        # set initial nodes
        start: Node = start_zone.upper_right_node
        cur: Node = start
        targ: Node = end_zone.upper_right_node

        # set initial values
        cur.g_value = 0.0
        cur.f_value = self.get_heuristic_estimate(cur, targ)
        self.priority_queue_push(cur, cur.f_value)

        # loop through neighnours
        while len(self.openList) > 0:
            cur = self.priority_queue_pop()


    print("Not Completed")
