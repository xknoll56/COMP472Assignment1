import numpy as np
from enum import Enum
import random

class Node():
	pass
class Edge():
	pass
class Zone():
	pass

class Diagonal(Enum):
	UP_RIGHT = 0
	DOWN_RIGHT = 1
	DOWN_LEFT = 2
	UP_LEFT = 3
	NONE = 4


class Cardinal(Enum):
	UP = 0
	RIGHT = 1
	DOWN = 2
	LEFT = 3
	NONE = 4

class Direction():
	def __init__(self, diag: Diagonal  = Diagonal.NONE, cardinal: Cardinal = Cardinal.NONE):
		self.diag = diag
		self.cardinal = cardinal
	

class Node():

	class CardinalConnection():
		def __init__(self, node: Node, edge: Edge):
			self.node = node
			self.edge = edge
	# e00 and e01 represent 1 path to the diagonal while e10 and e11 represent
	# the alternative path
	class DiagonalConnection():
		def __init__(self, node: Node, e00: Edge, e01: Edge, e10: Edge, e11: Edge):
			self.node = node
			self.e00 = e00
			self.e01 = e01
			self.e10 = e10
			self.e11 = e11
			
	def __init__(self, name: str, x:int, y:int):
		self.name: str = name
		self.x = x
		self.y = y


		#A list of all cardinal edges
		self.edges: list[Edge] = list()
		#A list of all the cardinal nodes
		self.cardinals :dict = dict()
		#A list of all the diagonals nodes
		self.diags: dict = dict()

		#Edge to the Right
		self.right_edge: Edge = None
		#Edge to Downward
		self.down_edge: Edge = None
		#Edge to the Left
		self.left_edge: Edge = None
		#Edge to Upward
		self.up_edge: Edge = None
		#To be used to find the path once the target is found
		self.prevNode: Node = None
		#To be used to for transition
		self.next: Node = None

		self.upper_node: Node = None
		self.upper_right_node: Node = None
		self.right_node: Node = None
		self.lower_right_node:Node = None
		self.lower_node: Node = None
		self.lower_left_node: Node = None
		self.left_node: Node = None
		self.upper_left_node: Node = None

		self.g_value: float = float('inf')
		self.f_value: float = float('inf')
		self.h_value: float = None

		self.q_limit = 15

	

	#cardinals will be checked by all the patients
	def has_right_edge(self):
		return self.right_edge != None
	def has_left_edge(self):
		return self.left_edge != None
	def has_upper_edge(self):
		return self.up_edge != None
	def has_lower_edge(self):
		return self.down_edge != None

	#diagonal checks will be used for the vaccinated patient 
	def has_upper_right_edge(self):
		return self.has_right_edge() and self.has_upper_edge()
	def has_upper_left_edge(self):
		return self.has_upper_edge() and self.has_left_edge()
	def has_lower_left_edge(self):
		return self.has_lower_edge() and self.has_left_edge()
	def has_lower_right_edge(self):
		return self.has_lower_edge() and self.has_right_edge()

class Edge():
	def __init__(self, node1: Node, node2: Node, side_zone_1: Zone = None, side_zone_2: Zone = None):
		self.node1: Node = node1
		self.node2: Node = node2
		self.side_zone_1: Zone = side_zone_1
		self.side_zone_2: Zone = side_zone_2
		self.dir: Direction = dir

	def __str__(self):
		s: str = str()
		s += "Edge has nodes connected: "+self.node1.name+" and "+self.node2.name+"\n"
		s += "\t zones connected: "
		if self.side_zone_1 is not None:
			s+=self.side_zone_1.zone_type+", "
		if self.side_zone_2 is not None:
			s+=self.side_zone_2.zone_type
		return s


class Zone():
	def __init__(self, x: int, y: int, zone_type: str, upper_left_node:Node = None, upper_right_node: Node = None, down_left_node: Node = None, down_right_node: Node = None):
		self.x: int = x
		self.y: int = y
		self.zone_type: str = zone_type
		#Upper Left Node
		self.upper_left_node: Node = upper_left_node
		#Upper Right Node
		self.upper_right_node: Node = upper_right_node
		#Down Right Node
		self.down_right_node: Node = down_right_node
		#Down Left Node
		self.down_left_node: Node = down_left_node

		self.neighboring_zones: list[Zone] = list()

class Map:
	# q = quarentine place, v = vaccinated place, p = playground, e = empty
	def __init__(self, rows: int = 3, columns: int = 4, grid_data =  [['q', 'v', 'p', 'e'],['v', 'e', 'q', 'e'], ['p', 'q', 'v', 'v']]):
		self.rows: int = rows
		self.columns: int = columns
		# Zones will be converted into a numpy 2d array of Zones
		self.zones = list(list())
		# A data member containing all of the edges
		self.edge_list: list[Edge] = list()

		# Generate the zones grid
		for i in range(len(grid_data)):
			self.zones.append(list())
			for j in range(len(grid_data[i])):
				self.zones[i].append(Zone(j, i, grid_data[i][j]))
			self.zones[i] = np.array(self.zones[i])
		self.zones = np.array(self.zones)

		# Generate the Nodes
		x = 65
		self.nodes = list(list())
		for i in range(self.rows+1):
			self.nodes.append(list())
			for j in range(self.columns+1):
				self.nodes[i].append(Node(chr(x), j, i))
				x+=1

		# Setting each node corresponding to the zone
		zone: Zone
		for i in range(self.rows):
			for j in range(self.columns):
				zone = self.zones[i][j]
				zone.upper_left_node = self.nodes[i][j]
				zone.upper_right_node = self.nodes[i][j+1]
				zone.down_left_node = self.nodes[i+1][j]
				zone.down_right_node = self.nodes[i+1][j+1]
				if j == 0:
					self.edge_list.append(Edge(self.nodes[i][j], self.nodes[i+1][j], None, self.zones[i][j]))
				else:
					self.edge_list.append(Edge(self.nodes[i][j], self.nodes[i+1][j], self.zones[i][j-1], self.zones[i][j]))
				if i == 0:
					self.edge_list.append(Edge(self.nodes[i][j], self.nodes[i][j+1], None, self.zones[i][j]))
				else:
					self.edge_list.append(Edge(self.nodes[i][j], self.nodes[i][j+1], self.zones[i-1][j], self.zones[i][j]))
			self.edge_list.append(Edge(self.nodes[i][self.columns], self.nodes[i+1][self.columns], self.zones[i][self.columns-1], None))
		for j in range(self.columns):
			self.edge_list.append(Edge(self.nodes[self.rows][j], self.nodes[self.rows][j+1], self.zones[self.rows-1][j], None))

		# Now setting the node lists, unoptimal method and will improve later
		e: Edge
		n: Node
		nOther: Node
		for nodeList in self.nodes:
			for n in nodeList:
				for e in self.edge_list:
					if n == e.node1 or n == e.node2:
						n.edges.append(e)
						if n == e.node1:
							nOther = e.node2
						elif n == e.node2:
							nOther = e.node1
						if nOther.x-n.x == 1:
							n.right_edge = e
						elif nOther.x-n.x == -1:
							n.left_edge = e
						elif nOther.y-n.y == 1:
							n.down_edge = e
						elif nOther.y-n.y == -1:
							n.up_edge = e
		n: Node
		e: Edge
		
		#final loop to set the node adgacency
		for nodeList in self.nodes:
			for n in nodeList:
				if n.has_right_edge():
					e = n.right_edge
					if e.node1 == n:
						n.right_node = e.node2
					else:
						n.right_node = e.node1
					n.cardinals[Cardinal.RIGHT] = Node.CardinalConnection(n.right_node, n.right_edge)
				if n.has_lower_edge():
					e = n.down_edge
					if e.node1 == n:
						n.lower_node = e.node2
					else:
						n.lower_node = e.node1
					n.cardinals[Cardinal.DOWN] = Node.CardinalConnection(n.lower_node, n.down_edge)
				if n.has_left_edge():
					e = n.left_edge
					if e.node1 == n:
						n.left_node = e.node2
					else:
						n.left_node = e.node1
					n.cardinals[Cardinal.LEFT] = Node.CardinalConnection(n.left_node, n.left_edge)
				if n.has_upper_edge():
					e = n.up_edge
					if e.node1 == n:
						n.upper_node = e.node2
					else:
						n.upper_node = e.node1
					n.cardinals[Cardinal.UP] = Node.CardinalConnection(n.upper_node, n.up_edge)
		zone: Zone
		#final loop to set the node diagonal adgacency
		for nodeList in self.nodes:
			for n in nodeList:
				if n.has_upper_right_edge():
					zone = self.get_diag_zone(n, Diagonal.UP_RIGHT)
					if zone is not None:
						n.upper_right_node = zone.upper_right_node

						n.diags[Diagonal.UP_RIGHT] = Node.DiagonalConnection(n.upper_right_node,   
							# f = finish, s = start
							# n -e01- f
							# |       |
							# e00     e11
							# |       |
							# s -e10- n
							e00 = zone.down_left_node.up_edge, 
							e01 = zone.upper_left_node.right_edge, 
							e10  = zone.down_left_node.right_edge, 
							e11 = zone.down_right_node.up_edge)
				if n.has_lower_right_edge():
					zone = self.get_diag_zone(n, Diagonal.DOWN_RIGHT)
					if zone is not None:
						n.lower_right_node = zone.down_right_node
						n.diags[Diagonal.DOWN_RIGHT] = Node.DiagonalConnection(n.lower_right_node,
							# s -e00- n
							# |       |
							# e10     e01
							# |       |
							# n -e11- f
							e00 = zone.upper_left_node.right_edge, 
							e01 = zone.upper_right_node.down_edge, 
							e10 = zone.upper_left_node.down_edge, 
							e11 = zone.down_left_node.right_edge)
				if n.has_lower_left_edge():
					zone = self.get_diag_zone(n, Diagonal.DOWN_LEFT)
					if zone is not None:
						n.lower_left_node = zone.down_left_node
						n.diags[Diagonal.DOWN_LEFT] = Node.DiagonalConnection(n.lower_left_node,
							# n -e00- s
							# |       |
							# e01     e10
							# |       |
							# f -e11- n
							e00 = zone.upper_right_node.left_edge,
							e01 = zone.upper_left_node.down_edge,
							e10 = zone.upper_right_node.down_edge,
							e11 = zone.down_right_node.left_edge)
				if n.has_upper_left_edge():
					zone = self.get_diag_zone(n, Diagonal.UP_LEFT)
					if zone is not None:
						n.upper_left_node = zone.upper_left_node
						n.diags[Diagonal.UP_LEFT] = Node.DiagonalConnection(n.upper_left_node, 
							 # f -e11- n
							 # |       |
							 # e01     e10
							 # |       |
							 # n -e00- s
							e00 = zone.down_right_node.up_edge,
							e01 = zone.upper_right_node.left_edge,
							e10 = zone.down_right_node.left_edge,
							e11 = zone.down_left_node.up_edge)
		zone:Zone
		#Finally need to set the zone adgacency for the role P
		for i in range(rows):
			for j in range(columns):
				zone = self.zones[i][j]
				if i > 0:
					zone.neighboring_zones.append(self.zones[i-1][j])
				if j > 0:
					zone.neighboring_zones.append(self.zones[i][j-1])
				if i < rows-1:
					zone.neighboring_zones.append(self.zones[i+1][j])
				if j < columns-1:
					zone.neighboring_zones.append(self.zones[i][j+1])

	@staticmethod
	def generate_random_map(columns: int, rows: int, max_type = None, max_amount = None):
		data = list()
		random.seed()
		max_type_locs = list()
		for i in range(max_amount):
			max_type_locs.append((random.randrange(0, rows-1), random.randrange(0, columns-1)))
		for i in range(rows):
			data.append(list())
			for j in range(columns):
				switcher = {
					0: 'q',
					1: 'v',
					2: 'p',
					3: 'e'
					}
				r = random.randrange(0, 4)
				c = switcher.get(r)
				if max_type is not None:                    
					while c is max_type:
						r = random.randrange(0, 4)
						c = switcher.get(r)
				data[i].append(c)
		for index in max_type_locs:
			data[index[0]][index[1]] = max_type
		return Map(rows, columns, data)


	def get_diag_zone(self, node: Node, diag: Diagonal):
		x = node.x
		y = node.y
		switcher1 = {
			Diagonal.DOWN_LEFT: -1,
			Diagonal.DOWN_RIGHT: 0,
			Diagonal.UP_LEFT: -1,
			Diagonal.UP_RIGHT: 0
			}
		x += int(switcher1.get(diag))
		switcher2 ={
			Diagonal.DOWN_LEFT: 0,
			Diagonal.DOWN_RIGHT: 0,
			Diagonal.UP_LEFT: -1,
			Diagonal.UP_RIGHT: -1
			}
		y += int(switcher2.get(diag))
		if y >= 0 and y< self.rows and x >= 0 and x < self.columns:
			return self.zones[y][x]
		else:
			return None

	def __str__(self):
		s:str = str()
		zone: Zone
		for i in range(len(self.zones)):
			for j in range(len(self.zones[i])):
				zone = self.zones[i][j]
				s += "("+str(zone.upper_left_node.x)+","+str(zone.upper_left_node.y)+")\t\t"
			s += "("+str(zone.upper_right_node.x)+","+str(zone.upper_right_node.y)+")\n\t"
			for j in range(len(self.zones[i])):
				zone = self.zones[i][j]
				s += zone.zone_type+"\t\t"
		return s

	@staticmethod
	def generate_defined_map(rows: int, cols: int, num_q: int = 1, num_v: int = 1, num_p: int = 1):
		print("Generating Defined Map of Size: " + str(rows) + " x " + str(cols))

		# Create empty map list
		data = [['e'] * rows for _ in range(cols)]

		# Zone Flag
		zone_placed: bool = False

		# Random Seed
		random.seed()

		num_zones = num_q + num_v + num_p
		left_q = num_q
		left_v = num_v
		left_p = num_p

		while num_zones > 0:
			zone_placed = False

			while zone_placed == False:

				# Generate random coordinates
				zone_row = random.randrange(0, rows)
				zone_col = random.randrange(0, cols)

				# Check if zone is empty
				if data[zone_row][zone_col] == 'e':
					print("Zone at position [" + str(zone_row) + "][" + str(zone_col) + "] was empty")
					# Check Zones left to place
					if left_q > 0:
						data[zone_row][zone_col] = 'q'
						left_q -= 1
						zone_placed = True
					elif left_v > 0:
						data[zone_row][zone_col] = 'v'
						left_v -= 1
						zone_placed = True
					elif left_p > 0:
						data[zone_row][zone_col] = 'p'
						left_p -= 1
						zone_placed = True
			print("Recalculating num_zones")
			num_zones = left_q + left_v + left_p 

		return Map(rows, cols, data)




def printMap(map:Map):
	edge: Edge
	z: Zone
	e: Edge
	n: Node
	for i in range(len(map.zones)):
		for j in range(len(map.zones[i])):
			z = map.zones[i][j]
			print("Zone "+str(z.x)+","+str(z.y))
			print("Upper left node: "+z.upper_left_node.name+" has edges: ")
			for e in z.upper_left_node.edges:
				print(e)
			print("\nUpper Right node: "+z.upper_right_node.name+" has edges: ")
			for e in z.upper_right_node.edges:
				print(e)
			print("\nDown left node: "+z.down_left_node.name+" has edges: ")
			for e in z.down_left_node.edges:
				print(e)
			print("\nDown Right node: "+z.down_right_node.name+" has edges: ")
			for e in z.down_right_node.edges:
				print(e)
			print("*************************NEXT ZONE****************************")

