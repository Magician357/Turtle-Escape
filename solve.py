# This file is not meant to be run. This is simply code to solve the maze.

direction_list = (0,1,2,3)
dx = (0,1,0,-1)
dy = (-1,0,1,0)
opposite = (2,3,0,1)

class solver:
    def __init__(self,maze):
        self.width,self.height = maze.width,maze.height
        self.directions=[[4 for _ in range(self.width)] for _ in range(self.height)]
        
        self.backlog=[(0,self.height-1)] # start point in bottom left corner
        
        self.checked = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.checked[self.backlog[0][1]][self.backlog[0][0]]=1
        self.directions[self.backlog[0][1]][self.backlog[0][0]]=2
        
        self.steps = 0

# Note:
#   For both the bfs and dfs algorithms, I figured out the algorithms a while
#   ago, and don't have anywhere I specifically got them from. This code was
#   written by me.

class bfs_solver(solver):
    def __init__(self,maze):
        super().__init__(maze)
    
    def step(self,maze,end_point):
        
        # Algorithm:
        #     While backlog is not empty
        #         Get oldest cell in backlog
        #         Add every valid neighbor to the backlog
        #         Log the direction to go backward from each neighbor
        #         Remove the cell
        
        if len(self.backlog) > 0:
            cx,cy = self.backlog[0] # oldest item
            for d in direction_list:
                nx=cx+dx[d] # Get new position
                ny=cy+dy[d]
                # If nx and ny are in bounds
                # and the cell is unvisited
                if nx >= 0 and ny >= 0 and nx < self.width and ny < self.height \
                    and self.directions[ny][nx] == 4 and maze[cx,cy][d] == 1 and self.checked[ny][nx] == 0:
                        self.backlog.append((nx,ny)) # add to list to be used again
                        self.directions[ny][nx]=opposite[d] # log path to point
                        if (nx,ny) == end_point:
                            self.backlog=[]
                            return True, (0,0)
            self.checked[cy][cx] = 1 # Log that it was visited
            self.backlog.pop(0) # Remove the cell (already checked)
            self.steps+=1
            return False, (cx,cy) # Return false as it is not finished
        return True, (0,0) # Return true as it is finished
    
class dfs_solver(solver):
    def __init__(self,maze):
        super().__init__(maze)
    
    def step(self,maze,end_point):
        # Algorithm:
        #     While backlog is not empty
        #         Get newest cell in backlog
        #         Add every valid neighbor to the backlog
        #         Log the direction to go backward
        #         Remove the cell
        
        remove_index = -1
        
        if len(self.backlog) > 0:
            cx,cy = self.backlog[-1] # newest item
            for d in direction_list:
                nx=cx+dx[d] # Get new position
                ny=cy+dy[d]
                # If nx and ny are in bounds
                # and the cell is unvisited
                if nx >= 0 and ny >= 0 and nx < self.width and ny < self.height \
                    and self.directions[ny][nx] == 4 and maze[cx,cy][d] == 1 and self.checked[ny][nx] == 0:
                        self.backlog.append((nx,ny)) # add to list to be used again
                        remove_index-=1 # save index of current item
                        self.directions[ny][nx]=opposite[d] # log path to point
                        if (nx,ny) == end_point:
                            self.backlog=[]
                            return True, (0,0)
            self.checked[cy][cx] = 1 # Log that it was visited
            self.backlog.pop(remove_index) # Remove the cell (already checked)
            self.steps+=1
            return False, (cx,cy) # Return false as it is not finished
        return True, (0,0) # Return true as it is finished

# Note:
#    Ideas taken from https://matteo-tosato7.medium.com/exploring-the-depths-solving-mazes-with-a-search-algorithm-c15253104899
#    May not be the exact astar algorithm, but it uses a similar or the same cost function.
#    How the cost function worked was the only thing taken, all other code was written by me.

class astar_solver(solver):
    def __init__(self,maze):
        super().__init__(maze)
        self.start_point = (0,self.height-1)
        self.backlog=set([(self.start_point,self.heuristic(self.start_point,(self.width-1,0)))]) # start point in bottom left corner
        # also store cost for each point
    def path_from(self,pos,cur_total=0):
        cx, cy=pos
        if pos == self.start_point or self.directions[cy][cx] == 4:
            # Reached end
            return cur_total
        else:
            # Recursively
            nx=cx+dx[self.directions[cy][cx]]
            ny=cy+dy[self.directions[cy][cx]]
            # Get path from previous
            return self.path_from((nx,ny),cur_total+1)
    def heuristic(self,pos1,pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    def cost(self,pos,end_pos):
        return self.heuristic(pos,end_pos)+self.path_from(pos)
    def step(self,maze,end_point):
        
        # Algorithm:
        #     While backlog is not empty
        #         Get cell with lowest cost
        #         Add every valid neighbor to the backlog
        #         Log the direction to go backward
        #         Remove the cell
        
        if len(self.backlog) > 0:
            
            cur = min(self.backlog,key=lambda x:x[1])
            
            cx,cy = cur[0] # oldest item
            for d in direction_list:
                nx=cx+dx[d] # Get new position
                ny=cy+dy[d]
                # If nx and ny are in bounds
                # and the cell is unvisited
                if nx >= 0 and ny >= 0 and nx < self.width and ny < self.height \
                    and self.directions[ny][nx] == 4 and maze[cx,cy][d] == 1 and self.checked[ny][nx] == 0:
                        self.backlog.add(((nx,ny),self.cost((nx,ny),end_point))) # add to list to be used again
                        self.directions[ny][nx]=opposite[d] # log path to point
                        if (nx,ny) == end_point:
                            self.backlog=[]
                            return True, (0,0)
            self.checked[cy][cx] = 1 # Log that it was visited
            self.backlog.remove(cur) # Remove the cell (already checked)
            self.steps+=1
            return False, (cx,cy) # Return false as it is not finished
        return True, (0,0) # Return true as it is finished

def propagate_path_from(cx,cy,curpath,sx,sy,directions):
    
    # Generates the next point in a path, following directions created by the solving algorithm

    direction=directions[int(cy)][int(cx)]
    if cx==sx and cy==sy:
        # Path has reached the end point
        return True, curpath, (sx,sy)
    else:
        # Calculate new position and return new list
        nx=cx+dx[direction]
        ny=cy+dy[direction]
        curpath.append((nx,ny))
        return False, curpath, (nx,ny)