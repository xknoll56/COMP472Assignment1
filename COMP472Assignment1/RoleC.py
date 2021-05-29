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

		travel_cost: float = 0.0
		# set initial nodes
		start: Node = start_zone.upper_right_node
		cur: Node = start
		targ: Node = end_zone.upper_right_node

		# set initial values
		cur.g_value = 0.0
		cur.f_value = self.get_heuristic_recursive(cur, targ)
		self.priority_queue_push(cur, cur.f_value)

		# algorithm start
		while len(self.openList) > 0:
			# set cur to node with lowest f_value
			cur = self.priority_queue_pop()

			# if cur is the goal node the algorithm exits
			if cur == targ:
				print("Target Node Reached")
				self.construct_path(start, cur)
				break

			# generate neighbours
			card: Node.CardinalConnection

			for card in cur.cardinals.values():
				n: Node = card.node
				# calculate g_value of neighbour
				tentative_g = cur.g_value + self.get_cost_cardinal(card.edge) + travel_cost
				# compare tentative_g to current g_value of node
				if tentative_g < n.g_value:
					n.prevNode = cur
					n.g_value = tentative_g
					n.f_value = n.g_value + self.get_heuristic_recursive(n, targ)
					if n not in self.openList:
						self.priority_queue_push(n, n.f_value)

		if len(self.openList) == 0:
			print("No path to goal")

	def construct_path(self, start: Node, cur: Node):
		self.path = []
		self.path.insert(0, cur)
		while cur != start:
			cur = cur.prevNode
			self.path.insert(0, cur)

	# This heuristic function takes into account the number of nodes travelled (adds +1 each time a node is travelled)
	def get_heuristic_recursive(self, cur_node: Node, targ: Node, prev_node: Node = None, cost: float = 0.0):
		travel_cost: float = 0.0

		if cur_node != targ:
			# calculate distance from start node to target node
			dx = targ.x - cur_node.x
			dy = targ.y - cur_node.y
			# determine direction the goal is from the start

			v: list[int] = [dx, dy]
			# normalize direction
			if dx != 0:
				v[0] = v[0] / abs(v[0])
			if dy != 0:
				v[1] = v[1] / abs(v[1])
			v = tuple(v)
			goal_dir = self.dir_switch.get(v)

			# recursive check based on direction to goal
			if dir == Cardinal.DOWN:
				# left move
				cost_left = self.cardinal_move(cur_node.left_node, cur_node, targ, cur_node.left_edge, cost)
				# right move
				cost_right = self.cardinal_move(cur_node.right_node, cur_node, targ, cur_node.right_edge, cost)
				# down move
				cost_down = self.cardinal_move(cur_node.lower_node, cur_node, targ, cur_node.down_edge, cost)
				# get minimum
				cost += min(cost_left, cost_right, cost_down)
			if dir == Cardinal.UP:
				# left move
				cost_left = self.cardinal_move(cur_node.left_node, cur_node, targ, cur_node.left_edge, cost)
				# right move
				cost_right = self.cardinal_move(cur_node.right_node, cur_node, targ, cur_node.right_edge, cost)
				# up move
				cost_up = self.cardinal_move(cur_node.upper_node, cur_node, targ, cur_node.up_edge, cost)
				# get minimum
				cost += min(cost_left, cost_right, cost_up)
			if dir == Cardinal.RIGHT:
				# up move
				cost_up = self.cardinal_move(cur_node.upper_node, cur_node, targ, cur_node.up_edge, cost)
				# down move
				cost_down = self.cardinal_move(cur_node.lower_node, cur_node, targ, cur_node.down_edge, cost)
				# right move
				cost_right = self.cardinal_move(cur_node.right_node, cur_node, targ, cur_node.right_edge, cost)
				# get minimum
				cost += min(cost_up, cost_down, cost_right)
			if dir == Cardinal.LEFT:
				# up move
				cost_up = self.cardinal_move(cur_node.upper_node, cur_node, targ, cur_node.up_edge, cost)
				# down move
				cost_down = self.cardinal_move(cur_node.lower_node, cur_node, targ, cur_node.down_edge, cost)
				# left move
				cost_left = self.cardinal_move(cur_node.left_node, cur_node, targ, cur_node.left_edge, cost)
				# get minimum
				cost += min(cost_up, cost_down, cost_left)
			if dir == Diagonal.DOWN_LEFT:
				# down move
				cost_down = self.cardinal_move(cur_node.lower_node, cur_node, targ, cur_node.down_edge, cost)
				# left move
				cost_left = self.cardinal_move(cur_node.left_node, cur_node, targ, cur_node.left_edge, cost)
				# get minimum
				cost += min(cost_down, cost_left)
			if dir == Diagonal.DOWN_RIGHT:
				# down move
				cost_down = self.cardinal_move(cur_node.lower_node, cur_node, targ, cur_node.down_edge, cost)
				# right move
				cost_right = self.cardinal_move(cur_node.right_node, cur_node, targ, cur_node.right_edge, cost)
				# get minimum
				cost += min(cost_down, cost_right)
			if dir == Diagonal.UP_LEFT:
				# up move
				cost_up = self.cardinal_move(cur_node.upper_node, cur_node, targ, cur_node.up_edge, cost)
				# left move
				cost_left = self.cardinal_move(cur_node.left_node, cur_node, targ, cur_node.left_edge, cost)
				# get minimum
				cost += min(cost_up, cost_left)
			if dir == Diagonal.UP_RIGHT:
				# up move
				cost_up = self.cardinal_move(cur_node.upper_node, cur_node, targ, cur_node.up_edge, cost)
				# right move
				cost_right = self.cardinal_move(cur_node.right_node, cur_node, targ, cur_node.right_edge, cost)
		
		# return when cur_node == targ
		return cost

	def cardinal_move(self, new_node: Node, cur_node: Node, prev_node: Node, targ_node: Node, travel_edge: Edge, cost: float):
		# if the node to travel to is the one that the path came from, return infinity to prevent backtracking
		if new_node == prev_node:
			return math.inf
		# otherwise recursive call get_heuristic_recursive
		cost_move = cost + self.get_cost_cardinal(travel_edge) + get_heuristic_recursive(new_node, targ, cur_node, cost) + travel_cost
		return cost_move
