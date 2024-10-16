import pygame
from random import randint

width, height = 800, 800
fps = 60

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

background_color=(255,255,255)


door_size = 40
maze_dist = 20

count = 0

# generate maze
lines = []
doors = []
distance = 600 # distance for line to go
x,y = 700,100 # current position
d=2 # directions, N=0 E=1 S=2 W=3
dx = (0,1,0,-1)
dy = (-1,0,1,0)
count=0
while distance > 0:
    nx,ny = x+distance*dx[d],y+distance*dy[d]
    lines.append(((x,y),(nx,ny)))
    if count > 4:
        if distance > door_size * 2.5:
            door_amount = randint(1,2)
            max_door_distance = distance//door_amount
            min_door_distance = 0
            for _ in range(door_amount):
                cur_door_size = door_size + randint(-5,5)
                door_pos = randint(min_door_distance,max_door_distance-cur_door_size)
                doorxA,dooryA = x+door_pos*dx[d],y+door_pos*dy[d]
                doorxB,dooryB = doorxA+cur_door_size*dx[d],dooryA+cur_door_size*dy[d]
                doors.append(((doorxA,dooryA),(doorxB,dooryB)))
        if distance > maze_dist * 4:
            if d == 0 or d == 2:
                bx,by = x, randint(min(y,ny)+door_size,max(y,ny)-door_size)
                nbx = bx + maze_dist*dy[d]*2
                lines.append(((bx,by),(nbx,by)))
    distance-=maze_dist
    d=(d+1)%4
    x,y=nx,ny
    count+=1



while running:
    # clear previous frame
    screen.fill(background_color)
    
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw maze
    for line in lines:
        pygame.draw.line(screen,(0,0,0),(line[0][0],line[0][1]),(line[1][0],line[1][1]),width=5)
        pygame.draw.circle(screen,(0,0,0),(line[0][0],line[0][1]),2.5)
        pygame.draw.circle(screen,(0,0,0),(line[1][0],line[1][1]),2.5)
    for door in doors:
        pygame.draw.line(screen,background_color,(door[0][0],door[0][1]),(door[1][0],door[1][1]),width=10)
        pygame.draw.circle(screen,background_color,(door[0][0],door[0][1]),5)
        pygame.draw.circle(screen,background_color,(door[1][0],door[1][1]),5)
    

    pygame.display.flip()

    clock.tick(fps)  # limit fps
