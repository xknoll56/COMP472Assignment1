from MapModule import *
import numpy as np
import math
import pygame
import sys
import threading
import queue
from RoleV import *
from RoleP import *
from RoleC import *

COMMANDS = queue.Queue()
running = 1

#class Input(threading.Thread):
#    def run(self):
#        while running:
#            command = input()
#            COMMANDS.put(command)
#INPUT: Input = Input()
#INPUT.start()


def draw_map(map: Map, v: Role):
    pygame.init()
    pygame.display.set_caption("A Star Path finding algorithm")
    BORDER = 50
    if(map.rows <= map.columns):
        WIDTH = 1024
        HEIGHT = int(1024 * map.rows * 0.5 / map.columns)
    else:
        WIDTH = int(768 * map.columns * 2 / map.rows)
        HEIGHT = 768
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = 1
    blue = (0, 0, 255)
    red = (255,0,0)
    green = (0, 255, 0)
    size = (WIDTH - 2 * BORDER) / map.columns
    
    playground = pygame.image.load("playground.jpg")
    pill = pygame.image.load("pill.jpg")
    virus = pygame.image.load("virus.jpg")
    empty = pygame.image.load("empty.jpg")

    playground = pygame.transform.scale(playground, (int(size), int(size * 0.5)))
    pill = pygame.transform.scale(pill, (int(size), int(size * 0.5)))
    virus = pygame.transform.scale(virus, (int(size), int(size * 0.5)))
    empty = pygame.transform.scale(empty, (int(size), int(size * 0.5)))
    pygame.display.set_icon(virus)
    image = {
    'p':playground,
    'q': virus,
    'v':pill,
    'e':empty
    }
    zoneRects = list(list())
    nodeCenter = []
    path = np.array(v.path)
   ## map.nodes[0][0].prevNode = map.nodes[1][1]
    for i in range(map.rows):
        zoneRects.append(list())
        for j in range(map.columns):
            rect: pygame.rect.Rect = playground.get_rect()
            zoneRects[i].append(rect)
            zoneRects[i][j].left = j * zoneRects[i][j].width + BORDER
            zoneRects[i][j].top = i * zoneRects[i][j].height + int(BORDER * map.rows * 0.5 / map.columns)
            nodeCenter.append(zoneRects[i][j].topleft)
            if j == map.columns - 1:
                nodeCenter.append(zoneRects[i][j].topright)
    for i in range(map.columns):
        nodeCenter.append(zoneRects[map.rows-1][i].bottomleft)
    nodeCenter.append(zoneRects[map.rows-1][map.columns-1].bottomright)
    nodeCenter = np.array(nodeCenter)
    font = pygame.font.SysFont("comicsansms", 12)
    text = font.render("Hello, World", True, (0, 128, 0))
    coord_to_index = lambda x, y : x+y*(map.columns+1)
    lerp = lambda x1, y1, x2, y2, t: (int(x1+(x2-x1)*t), int(y1 + (y2-y1)*t))
    drawn = 0
    ticksLastFrame = 0
    elapsed = 0.0
    #path = [map.zones[0][0].upper_left_node]
    while running:      
       # screen.blit(text,(0, 0))
        #try:
        #    command = COMMANDS.get(False)
        #except queue.Empty:
        #    command = None
        #if command:
        #    print("Printing command: "+command)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                print("Quiting application")
                pygame.quit()
                running = 0
                sys.exit(running)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    running = 0
                    INPUT.join()
                    INPUT.signal
                    sys.exit(running)


        #Draw the background
        if not drawn:
            screen.fill((200 , 200, 200))
            i: int = 0
            j: int = 0
            for rectList in zoneRects:
                for rect in rectList:
                    z = image.get(map.zones[i][j].zone_type)
                    if z is not None:
                        screen.blit(z, rect)
                    j+=1
                j = 0
                i+=1
            edge: Edge 
            for edge in map.edge_list:
                index1 = coord_to_index(edge.node1.x,edge.node1.y)
                index2 = coord_to_index(edge.node2.x, edge.node2.y)
                pygame.draw.line(screen, green, nodeCenter[index1], nodeCenter[index2], int(0.04*size))
            for i in range(len(nodeCenter)):
                pygame.draw.circle(screen, blue, nodeCenter[i], 0.04*size)
                #if i > 0:
                    #pygame.draw.line(screen, green, nodeCenter[i-1], nodeCenter[i])
            skip = 1
            for n in path:
                if not skip:
                    center1 = nodeCenter[coord_to_index(n.x, n.y)]
                    center2 = nodeCenter[coord_to_index(n.prevNode.x, n.prevNode.y)]
                    pygame.draw.line(screen, blue, center1, center2, int(0.04*size))
                skip  = 0

            ticksLastFrame = pygame.time.get_ticks()
            drawn = 1

        t = pygame.time.get_ticks()
        deltaTime = (t - ticksLastFrame)/1000.0
        elapsed += deltaTime*2.0
        ticksLastFrame = t
        if elapsed < len(path)-1:
            n = path[int(elapsed)+1]
            center1 = nodeCenter[coord_to_index(n.x, n.y)]
            center2 = nodeCenter[coord_to_index(n.prevNode.x, n.prevNode.y)]
            #pygame.draw.circle(screen, red, lerp(center2[0], center2[1], center1[0], center1[1], elapsed-int(elapsed)), 0.02*size)
        if elapsed > len(path):
            drawn = 0
            elapsed = 0.0

        

