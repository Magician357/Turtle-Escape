# This file is not meant to be run. This is simply code to solve the maze.

direction_list = (0,1,2,3)
dx = (0,1,0,-1)
dy = (-1,0,1,0)
opposite = (2,3,0,1)

class bfs_solver:
    def __init__(self,maze):
        self.width,self.height = maze.width,maze.height
        self.directions=[[4 for _ in range(self.width)] for _ in range(self.height)]
        
        self.backlog=[(0,self.height-1)] # start point in bottom left corner
        
        self.checked = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.checked[self.backlog[0][1]][self.backlog[0][0]]=1
        self.directions[self.backlog[0][1]][self.backlog[0][0]]=2
    
    def step(self,maze,end_point):
        
        # Algorithm:
        #     While backlog is not empty
        #         Get oldest cell in backlog
        #         Add every valid neighbor to the backlog
        #         Log the direction to go backward
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