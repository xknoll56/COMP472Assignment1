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



def main():
    #mat = np.array(np.array())
   # map = Map.generate_random_map(8, 8)
    #write_to_file("test.txt", map)
    map = load_from_file("test.txt")
    #map = Map()
    v = RoleV(map)
    bot_left: Zone = map.zones[0][map.columns-1]
    top_right: Zone = map.zones[map.rows-1][0]

    start = time.time()
    v.generate_closest_path(map.zones[3][3])  # TODO end points are chosen by the user.
    print("Time taken: "+str(time.time()-start))
    # print(v.path[len(v.path)-1].g_value)
    print(map)
    zone: Zone
    end_locations: list[Zone] = list()
    for zones in map.zones:
        for zone in zones:
            if zone.zone_type == 'v':
                end_locations.append(zone)
    
    print("Here are ")
    for loc in end_locations:
        print(str(loc.x)+","+str(loc.y))
    draw_map(map, v)

# Test main function
# def main():
#     map = load_from_file("test.txt")
#     v = RoleP(map)
#     print(v.get_heuristic(map.zones[1][1].upper_left_node, map.zones[2][3].down_right_node))

main()



