# This file is not meant to be run. This is simply code to generate mazes.

from random import randint, shuffle

# Cells of the maze are organized like this:
# [North, East, South, West, display, extra1, extra2]
# Where each direction represents if it is open (1) or closed (0)
# Extra is for any other data needed by the algorithm.

dx = (0,1,0,-1)
dy = (-1,0,1,0)
opposite = (2,3,0,1)

class maze:
    def __init__(self,width,height):
        self.width,self.height = width,height
        self.grid = [[[0,0,0,0," ",0,0] for _ in range(width)] for _ in range(height)]
        
    def __getitem__(self,pos):
        x,y=pos
        return self.grid[y][x]
    
    def __setitem__(self,pos,newval):
        x,y=pos
        self.grid[y][x]=newval
        
    def open(self,x,y,dir,newval=1):
        # Open the wall
        self.grid[y][x][dir] = newval
        
        # If on an edge and the direction points out
        if (dir == 0 and y == 0) \
            or (dir == 1 and x == self.width-1) \
                or (dir == 2 and y == self.height-1) \
                    or (dir == 3 and x == 0):
                        pass
        else:
            # Open the adjacent cell
            self.grid[y+dy[dir]][x+dx[dir]][opposite[dir]] = newval
    
    @property
    def display(self):
        # Turn maze into ascii
        # First line
        final="+"
        final+="-"*((self.width*3)-1)
        final+="+"
        final+="\n"
        for row in self.grid:
            # Generate both the row and line below
            curA="|" # Actual row
            curB="+" # Line
            for cell in row:
                curA+=cell[4]+" " # Add display
                # If closed add wall, otherwise don't
                curA+="|" if cell[1] == 0 else " "
                curB+="--" if cell[2] == 0 else "  "
                curB+="+"
            final+=curA+"\n"+curB+"\n"
        return final
    
    def random_doors(self,amount=10):
        for _ in range(amount):
            self.open(randint(1,self.width-2),randint(1,self.height-2),randint(0,3))

def generate_maze_growing_tree(width,height,choosing_algorithm):
    # Extra1 will be how many times the cell was checked (in index 5)
    
    # Algorithm taken from https://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm
    # I didn't take any code from there, only the algorithm.
    
    # Algorithm:
    #  Create list C with one cell inside
    #  While C is not empty
    #       Choose a point
    #       Check every direction to see if there is an unvisited cell
    #         If there is, open a passage and add it to C
    #         If there isn't, remove the point from C
    
    # List with point
    C=[(randint(0,width-1),randint(0,height-1))]
    used=[] # Cells already used
    cur_maze=maze(width,height) # Create maze
    directions = [0,1,2,3] # List for directions
    while len(C) > 0: # While still cells
        # Choose an index
        cur_index = choosing_algorithm(len(C))
        # Get the x and y
        x,y = C[cur_index]
        # Log that this cell was visited
        cur_maze[x,y][5]+=1
        # Shuffle directions for more randomness
        shuffle(directions)
        found=False
        for d in directions:
            nx,ny=x+dx[d],y+dy[d]
            if nx < 0 or nx>=width or ny < 0 or ny>=height:
                continue # out of bounds
            elif (nx,ny) in used:
                continue # already went there
            elif cur_maze[x,y][d] == 1:
                continue # already opened
            elif cur_maze[nx,ny][5] > 0:
                continue # already visited
            else:
                # Open a path and continue
                cur_maze.open(x,y,d)
                C.append((nx,ny))
                cur_maze[nx,ny][5]+=1
                found=True
                break
        used.append((x,y))
        if not found:
            # If no unvisited cells, remove it
            C.pop(cur_index)
    
    # Open a few random doors to add more paths
    cur_maze.random_doors((width*height)//45)
    
    return cur_maze

choose_counter = 0
def choosing_algorithm(length):
    # Cycles between first, middle, and last
    global choose_counter
    choose_counter = (choose_counter+1)%4
    return (length-1,length//2,0,length-1)[choose_counter]

if __name__ == "__main__":
    test_maze = generate_maze_growing_tree(10,10,choosing_algorithm)
    print(test_maze.display)
    print("THIS FILE IS NOT MEANT TO BE RUN ON ITS OWN")