import pygame
from random import randint
from maze import generate_maze_growing_tree, choosing_algorithm
from solve import bfs_solver, propagate_path_from
import sys

# Declare variables
width, height = 900, 800
maze_width = 35
maze_height = 25
fps = 60

background_color=(255,255,255)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

pygame.font.init()
font = pygame.font.SysFont('Arial', 18)
def draw_text(text:str,pos,screen,font=font,color=(0,0,0)):
    # Draws text
    text_surface = font.render(text, False, color)
    screen.blit(text_surface,pos)

# Convert cell coordinates to screen coordinates
def tCell_to_pos(pos,center=True):
    cx,cy=pos
    offset=(0.5 if center else 0)
    return (50+(line_width*(cx+offset)),50+(line_height*(cy+offset)))

# Generate the maze
maze = generate_maze_growing_tree(maze_width,maze_height,choosing_algorithm)
print(maze.display)

# Open the start and end sides
maze.open(0,maze_height-1,2)
maze.open(maze_width-1,0,0)

# Create the solver
solver = bfs_solver(maze)

# Calculate sizes for the maze
line_width=(width-100)/maze_width
line_height=(height-100)/maze_height
print(line_width,line_height)

# Load the arrow picture
arrow=pygame.transform.scale(pygame.image.load("arrow_right.png"),(line_width-2,line_height-2))

start_rect = pygame.rect.Rect(*tCell_to_pos((0,maze_height-1),False),line_width,line_height)
end_rect = pygame.rect.Rect(*tCell_to_pos((maze_width-1,0),False),line_width,line_height)

# Initialize variables for drawing
amount_draw=0
cur_amount =0

# For debug, not currently used
dir_string = ("N","E","S","W","#")

# Initialize solver variables
path = []
cx,cy = (maze_width-1,0)
end_point= tCell_to_pos((cx,cy))

finished = False

space_pressed = False

while running:
    # clear previous frame
    screen.fill(background_color)
    
    pressed = pygame.key.get_pressed()
    
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    if pressed[pygame.K_SPACE]:
        if not space_pressed:
            space_pressed = True
            
            # Generate the maze
            maze = generate_maze_growing_tree(maze_width,maze_height,choosing_algorithm)
            print(maze.display)

            # Open the start and end sides
            maze.open(0,maze_height-1,2)
            maze.open(maze_width-1,0,0)
            
            # Initialize variables for drawing
            amount_draw=0
            cur_amount =0
            
            # Create the solver
            solver = bfs_solver(maze)
            
            cx,cy = (maze_width-1,0)
            path = []
            
            finished = False
    else:
        space_pressed=False

    # draw start and end squares
    pygame.draw.rect(screen,(100,255,100),start_rect)
    pygame.draw.rect(screen,(255,150,150),end_rect)

    # draw maze
    cur_amount = 0
    lines = []
    for n, row in enumerate(maze.grid):
        curY=50+(line_height*(n)) # Calculate current y
        for i, cell in enumerate(row):
            curX=50+(line_width*(i)) # Calculate current x
            
            # If the cell has been visited by the solver
            # And the path isn't finished or s is pressed
            if solver.directions[n][i] != 4 and (not finished or pressed[pygame.K_s]):
                if (n == 0 and i == maze_width-1) or (i == 0 and n == maze_height-1):
                    # Do not draw start and end square
                    pass
                else:
                    # Draw green square
                    cell_rect = pygame.rect.Rect(curX,curY,line_width,line_height+2)
                    pygame.draw.rect(screen,(200,255,200),cell_rect)
                # Draw arrow
                rotated_arrow = pygame.transform.rotate(arrow,-90*(solver.directions[n][i]-1))
                screen.blit(rotated_arrow,(curX+1,curY+1))
                # draw_text(dir_string[solver.directions[n][i]],(curX+line_width/2,curY+line_height/2),screen)
            
            # Drawn after so the lines are over the green boxes
            if cell[1] == 0:
                # Wall on side
                lines.append(((curX+line_width,curY),(curX+line_width,curY+line_height)))
            if cell[2] == 0:
                # Wall on bottom
                lines.append(((curX,curY+line_height),(curX+line_width,curY+line_height)))
            cur_amount+=1
            
            # Stop if exceeding current draw amount
            if cur_amount > amount_draw: break
        if cur_amount > amount_draw: break
    
    
    for line in lines:
        # Draw every line
        pygame.draw.line(screen,0,(line[0][0],line[0][1]),(line[1][0],line[1][1]),width=2)
    # Draw final lines on the side
    pygame.draw.lines(screen,0,False,[(50,50+line_height*maze.height),(50,50),(50+line_width*(maze.width-1),50)],width=2)
    
    if amount_draw < maze_width*maze_height:
        # Increase the amount of cells to draw
        draw_text("Drawing maze",(10,25),screen)
        amount_draw+=randint(maze_width//8,maze_width//3)
    else:
        # Tick the solver
        solved, pos = solver.step(maze,(maze_width-1,0))
        if solved: # If finished solving
            # Grow the current path
            finished, path, new_pos = propagate_path_from(cx,cy,path,0,maze_height-1,solver.directions)
            cx,cy=new_pos
            
            # Draw the path
            pygame.draw.lines(screen,(10,100,255),False,[(end_point[0],end_point[1]-line_height),end_point]+[tCell_to_pos(position) for position in path]+([tCell_to_pos((0,maze_height))] if finished else []),width=3)
            # Append on the end point, and below the start point if finished
            if not finished:
                draw_text("Creating path",(10,25),screen)
            else:
                draw_text("Finished. Press S to unhide directions.",(10,25),screen)
        else:
            # Draw circle where the solver is checking
            draw_text("Creating directions",(10,25),screen)
            pygame.draw.circle(screen,(10,100,255),tCell_to_pos(pos),5)

    draw_text("Maze generated using growing tree algorithm. Solved using breadth first search.  Press space to reset.",(10,10),screen)

    pygame.display.flip()
    pygame.display.set_caption(f"Simple Maze Generator and Solver      Tps: {clock.get_fps():.2f}")

    clock.tick(fps)  # limit fps
