#  Tucil3StrAlgo_13517035_13517080
#  Hilmi Naufal Yafie - 13517080
#  Mgs. Muhammad Riandi Ramadhan - 13517080

import pygame
import math

pygame.init()
global black, white
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

# get size of maze
def getMazeScale() :
    with open('input.txt') as maze_file :
        maze_scale = sum(1 for row in maze_file)
    return maze_scale

# create maze
def createMaze(wall, path, start, finish) :
    maze_file = open("input.txt", "r")
    start_found = False
    for y, row in enumerate(maze_file) :
        
        for x, column in enumerate(row) :
            # if it is path
            if (column == '0') :
                path.append([x, y])
                # define start
                if (not(start_found)) :
                    if ((y == 0) or (y == getMazeScale()-1)) :
                        start.append(x)
                        start.append(y)
                        start_found = True
                    elif ((x == 0) or (x == getMazeScale()-1)) :
                        start.append(x)
                        start.append(y)
                        start_found = True
                # define finish
                elif (start_found) :
                    if ((y == 0) or (y == getMazeScale()-1)) :
                        finish.append(x)
                        finish.append(y)
                    elif ((x == 0) or (x == getMazeScale()-1)) :
                        finish.append(x)
                        finish.append(y)
            # if it is wall        
            else :
                wall.append([x, y])

# find candidate of next visited point
def findAdjacentList(recent_pos, waiting) :
    # check right side
    if ([recent_pos[0]+1, recent_pos[1]] in path) and ([recent_pos[0]+1, recent_pos[1]] not in visited) :
        waiting.append([recent_pos[0]+1, recent_pos[1]])
    # check bottom side
    if ([recent_pos[0], recent_pos[1]+1] in path) and ([recent_pos[0], recent_pos[1]+1] not in visited) :
        waiting.append([recent_pos[0], recent_pos[1]+1])
    # check left side
    if ([recent_pos[0]-1, recent_pos[1]] in path) and ([recent_pos[0]-1, recent_pos[1]] not in visited) :
        waiting.append([recent_pos[0]-1, recent_pos[1]])
    # check top side
    if ([recent_pos[0], recent_pos[1]-1] in path) and ([recent_pos[0], recent_pos[1]-1] not in visited) :
        waiting.append([recent_pos[0], recent_pos[1]-1])

#BFS
def BFSSearching(start,visited,waiting) :
    recent_pos = start
    while (recent_pos != finish) :
        findAdjacentList(recent_pos, waiting)
        
        adj_count = 0
        # check right side
        if ([waiting[0][0]+1, waiting[0][1]] in visited):
            adj_count += 1
        # check left side
        if ([waiting[0][0]-1, waiting[0][1]] in visited):
            adj_count += 1
        # check bottom side
        if ([waiting[0][0], waiting[0][1]+1] in visited):
            adj_count += 1
        # check top side
        if ([waiting[0][0], waiting[0][1]-1] in visited):
            adj_count += 1
        
        if (adj_count<2):
            # change to visited
            visited.append(waiting[0])
            # renew recent position
            recent_pos = waiting[0]
            # delete from waiting list
        
        del waiting[0]

#A*
def AStarSearching(start,visited,waiting) :
    recent_pos = start
    while (recent_pos != finish) :
        findAdjacentList(recent_pos, waiting)
    # findNextPosition(visited, waiting)
        priority = 999
        for idx, pos in enumerate(waiting) :
        # f(n) = g(n) + h(n)
            priority_temp = 1 + math.sqrt((finish[0]-pos[0])**2 + (finish[1]-pos[1])**2)
            if (priority_temp < priority) :
                priority = priority_temp
                choosen_idx = idx
        # change to visited
        visited.append(waiting[choosen_idx])
        # renew recent position
        recent_pos = waiting[choosen_idx]
        # delete from waiting list
        del waiting[choosen_idx]

#Clearing the path that not affected from start to finish
def ClearUnusedPath(visited, finish) :
    i = 0
    while i < len(visited) :
        if (visited[i] != start) and (visited[i] != finish) :
            adj_count = 0
        # check right side
            if ([visited[i][0]+1, visited[i][1]] in visited):
                adj_count += 1
        # check left side
            if ([visited[i][0]-1, visited[i][1]] in visited):
                adj_count += 1
        # check bottom side
            if ([visited[i][0], visited[i][1]+1] in visited):
                adj_count += 1
        # check top side
            if ([visited[i][0], visited[i][1]-1] in visited):
                adj_count += 1
        
            if (adj_count < 2) :
                visited.remove(visited[i])
                i = 0
            else :
                i += 1
        else :
            i += 1

def maze_display(maze_scale, visited, wall,path):

    displayExit = False

    WALL_LENGTH = 10

    mazeDisplay.fill(white)
    
    for i in range(maze_scale):   
        for j in range(maze_scale):
            #letak draw sesuai index i j
            y=WALL_LENGTH*j 
            y2=WALL_LENGTH
            x=i*WALL_LENGTH
            x2=WALL_LENGTH  
            
            if [i, j] in wall:
                pygame.draw.rect(mazeDisplay,black,(x,y,x2,y2))
            elif [i,j] in visited:
                pygame.draw.rect(mazeDisplay,red,(x,y,x2,y2))
            else:
                x=x2

    while not displayExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: displayExit = True

        pygame.display.update()
        clock.tick(30)

# MAIN PROGRAM
wall = []       # store point of wall
path = []       # store point of path
start = []      # store start point
finish = []     # store finish point
waiting = []    # store waiting point before visited 
visited = []    # store visited point

createMaze(wall, path, start, finish)
recent_pos = start
visited.append(start)
choose = int(input("Pilih Algoritma (1. BFS; 2. A*) : "))
if (choose == 1) :
    BFSSearching(start,visited,waiting)
elif (choose == 2) :
    AStarSearching(start,visited,waiting)
else :
    print("Input Salah")
    exit
ClearUnusedPath(visited,finish)     #bersihin path yang ga dipake

maze_scale = getMazeScale()
display_width = (maze_scale*10)     #lebar maze
display_height = (maze_scale*10)    #tinggi maze
mazeDisplay = pygame.display.set_mode((display_width,display_height))   #set display
clock = pygame.time.Clock()
maze_display(maze_scale, visited, wall,path)    #gambar maze
pygame.quit()
quit()