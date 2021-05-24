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
   # mat = np.array(np.array())
    #map = Map.generate_random_map(18, 20)
    #write_to_file("test.txt", map)
    map = load_from_file("test.txt")
    #map = Map()
    v = RoleV(map)
    bot_left: Zone = map.zones[0][0]
    top_right: Zone = map.zones[map.rows-1][map.columns-1]

    start = time.time()
    v.generate_path(bot_left, top_right)
    print("Time taken: "+str(time.time()-start))
    print(v.path[len(v.path)-1].g_value)

    draw_map(map, v)


main()



