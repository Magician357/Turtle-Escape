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
        # If tried to open an edge
        
        self.grid[y][x][dir] = newval
        
        if (dir == 0 and y == 0) \
            or (dir == 1 and x == self.width-1) \
                or (dir == 2 and y == self.height-1) \
                    or (dir == 3 and x == 0):
                        pass
        else:
            self.grid[y+dy[dir]][x+dx[dir]][opposite[dir]] = newval
    
    @property
    def display(self):
        final="+"
        final+="-"*((self.width*3)-1)
        final+="+"
        final+="\n"
        for row in self.grid:
            curA="|"
            curB="+"
            for cell in row:
                curA+=cell[4]+" "
                curA+="|" if cell[1] == 0 else " "
                curB+="--" if cell[2] == 0 else "  "
                curB+="+"
            final+=curA+"\n"+curB+"\n"
        return final
    
    # def crop(self):
    #     # cuts off top and bottom rows
    #     print(self.display)
    #     self.grid = self.grid[1:-1]
    #     for n in range(self.width):
    #         self.open(n,0,0,0) # close top
    #         self.open(n,-1,2,0) # close bottom
    #     print(self.display)
    #     self.height-=2

def generate_maze_growing_tree(width,height,choosing_algorithm):
    # Extra1 will be how many times the cell was checked (in index 5)
    
    # Algorithm taken from https://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm
    # Although, I didn't take any code from there.
    
    # Algorithm:
    #  Create list C with one cell inside
    #  While C is not empty
    #       Choose a point
    #       Check every direction to see if there is an unvisited cell
    #         If there is, open a passage and add it to C
    #         If there isn't, remove the point from C
    
    # This line isn't used
    # height += 2
    
    C=[(randint(0,width-1),randint(0,height-1))]
    used=[]
    cur_maze=maze(width,height)
    directions = [0,1,2,3]
    while len(C) > 0:
        cur_index = choosing_algorithm(len(C))
        x,y = C[cur_index]
        cur_maze[x,y][5]+=1
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
                cur_maze.open(x,y,d)
                C.append((nx,ny))
                cur_maze[nx,ny][5]+=1
                found=True
                break
        used.append((x,y))
        if not found:
            C.pop(cur_index)
    
    # This line isn't used
    # cur_maze.crop()
    
    return cur_maze

choose_counter = 0
def choosing_algorithm(length):
    global choose_counter
    choose_counter = (choose_counter+1)%3
    return (length-1,length//2,0)[choose_counter]

if __name__ == "__main__":
    test_maze = generate_maze_growing_tree(10,10,choosing_algorithm)
    print(test_maze.display)