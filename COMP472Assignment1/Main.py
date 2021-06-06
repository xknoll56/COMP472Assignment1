from RoleV import *
from RoleP import *
from RoleC import *
from Graphics import *
import time

def load_from_file(path: str):
	file = open(path, "r")
	line = file.readline().split(" ")
	columns = int(line[0])
	rows = int(line[1])
	data = []
	
	while line:
		line = file.readline()
		if line:
			data.append(line.split(" "))
	for i in range(len(data)):
		data[i] = data[i][:columns]
	data = data[:rows]
	return Map(rows, columns, data)


def write_to_file(path: str, map: Map):
	file = open(path, "w")
	file.write(str(map.columns)+" "+str(map.rows) + "\n")
	for zone_arr in map.zones:
		for zone in zone_arr:
			file.write(zone.zone_type+" ")
		file.write("\n")
	file.close()

def draw_map_guide(rows: int, cols: int):

	print("Zone Guide:")
	
	base_bar = "-----"
	bar = ""
	# Horizontal Bar Size
	for x in range(cols):
		bar += base_bar
	bar += "-"

	for y in range(rows):
		print(bar)
		row = "|"
		for x in range(cols):
			zone_num = (y * cols) + x
			if zone_num < 10:
				row += ("  " + str(zone_num) + " |")
			else:
				row += (" " + str(zone_num) + " |")
		print(row)
	print(bar)

def draw_node_guide():
	print("1-------2")
	print("|       |")
	print("|   0   |")
	print("|       |")
	print("3-------4")


def main():
	#mat = np.array(np.array())
	# map = Map.generate_random_map(8, 8, "p", 8)
	# write_to_file("test.txt", map)
	map = load_from_file("test.txt")
	#map = Map()
	v = RoleP(map)
	bot_left: Zone = map.zones[0][map.columns-1]
	top_right: Zone = map.zones[map.rows-1][0]

	start = time.time()
	#v.generate_path_closest(map.zones[map.rows//2][map.columns//2])  # TODO end points are chosen by the user.
	v.generate_path_closest(top_right)
	print("Time taken: "+str(time.time()-start))
	# print(v.path[len(v.path)-1].g_value)
	#print(map)
	draw_map(map, v)

# Test main function
# def main():
#     map = load_from_file("test.txt")
#     v = RoleP(map)
#     print(v.get_heuristic(map.zones[1][1].upper_left_node, map.zones[2][3].down_right_node))


def main_final():
	print("COMP472 - Assignment 1 - Covid Map Simulation")

	map: Map
	role: Role
	zone_num: int
	choice: int = int(input("Enter 1 to generate a map, or 2 to load a demo map: "))
	if choice == 1:
		# User Input for Max Dimensions
		map_rows = int(input("Enter desired map rows: "))
		map_cols = int(input("Enter desired map cols: "))
		max_zones = map_rows * map_cols

		# User Input for Zone Amounts
		num_q = int(input("Enter number of Quarantine Zones (Max: " + str(max_zones) + "): "))
		max_zones -= num_q
		num_v = int(input("Enter number of Vaccines Zones (Max: " + str(max_zones) + "): "))
		max_zones -= num_v
		num_p = int(input("Enter number of Playground Zones (Max: " + str(max_zones) + "): "))
		
		# Generate Map
		map: Map = Map.generate_defined_map(map_rows, map_cols, num_q, num_v, num_p)
		#write_to_file("demo_p.txt", map)
		# Prompt user for Role
		role_switch = {
			1: RoleC,
			2: RoleV,
			3: RoleP
			}
		role = role_switch.get(int(input("Enter Desired Role (1: RoleC, 2: RoleV, 3: RoleP): ")))
		role = role(map)
		# Prompt user for starting zone
		zone_num = int(input("Enter starting zone: "))
	elif choice == 2:
		choice = int(input("Enter Desired Role (1: RoleC, 2: RoleV, 3: RoleP): "))
		if choice == 1:
			map = load_from_file("demo_c.txt")
			role = RoleC(map)
			zone_num = 0
		elif choice == 2:
			map = load_from_file("demo_v.txt")
			role = RoleV(map)
			zone_num = 0
		elif choice == 3:
			map = load_from_file("demo_p.txt")
			role = RoleP(map)
			zone_num = 0

	# TODO: Print text map
	draw_map_guide(map.rows, map.columns)


	zone_row = math.floor(zone_num / map.columns)
	zone_col = (zone_num) % map.rows

	zone: Zone = map.zones[zone_row][zone_col]

	# Prompt Role P user for start position
	if isinstance(role, RoleP):
		draw_node_guide()
		node_switch = {
			0: zone,
			1: zone.upper_left_node,
			2: zone.upper_right_node,
			3: zone.down_left_node,
			4: zone.down_right_node
			}
		start = node_switch.get(int(input("Enter Starting Position: ")))
	else:
		start = zone

	start_time = time.time()
	role.generate_path_closest(start)

	print("Time Taken: " + str(time.time() - start_time))

	draw_map(map, role)


#main()
main_final()
	



