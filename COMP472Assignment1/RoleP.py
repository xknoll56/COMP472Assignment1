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
        pass


