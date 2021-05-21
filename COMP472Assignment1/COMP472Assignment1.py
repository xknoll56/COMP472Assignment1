from RoleV import *

def main():
    #map = Map.generate_random_map(15, 20)
    map = Map()
    v = RoleV(map)
    bot_left: Zone = map.zones[map.rows-1][0]
    top_right: Zone = map.zones[0][map.columns-1]
    v.generate_path(bot_left, top_right)
    node: Node
    for node in v.path:
        print(node.name)

  

main()



