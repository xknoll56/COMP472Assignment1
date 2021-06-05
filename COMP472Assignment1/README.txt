COMP 472 - A1
name - XXXXXXXX (Role C)
Xavier Knoll - 40132134 (Role V)
Jordan Goulet - 40075688 (Role P)

Summary:
This program calculates the path with the least cost from the chosen starting point to the closest possible destination.

App Flow:
0. The user is asked to generate a map, or load a demo map based on a role chosen.
1. The user is prompted to enter the desired number of rows and columns.
2. The user is prompted to enter the desired number of each type of zones (the remainder are set the the empty zone type).
3. A map is randomly generated according to the parameters provided by the user.
4. The user is prompted to select a role, C, V, or P.
5. The user is prompted to select a starting position.
6. The program uses an A* algorithm to calculate the least costly path to a destination of the role.
7. The program displays the total cost of the computed path (if a path with cost < inf exits).
8. The map and the generated path (if any) are displayed in a graph made in PyGame.
9. The program terminates when the user closes the map graph rendering window.

Structure and Libraries:
Main.py - controls the flow of the program.
MapModule.py - defines the classes related the the map (Map, Node, Zone, Edge, etc.).
Graphics.py - handles the drawing and rendering of the map and path with PyGame through the draw_map function.
Role.py - parent class of shared between all roles, implements the priority queue used for the A* algorithm.
RoleC.py - seeks a quarantine zone.
RoleV.py - seeks a vaccine zone.
RoleP.py - seeks a playground zone.