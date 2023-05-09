import numpy as np
import math
from obstacle_gen_gazebo import obs_coord
import pygame
import sys

sys.setrecursionlimit(4000)
goal_sample_rate = 0.05     #Sample rate to control randomness
MAP_WIDTH = 599             #Map dimenions
MAP_HEIGHT = 199
step_length = 20            #Step length for RRT connect
ROBOT_RADIUS = 0.25         #Robot radius

class Node:
    def __init__(self):
        self.state = None   #Current state [x,y] coordinates
        self.parent = None  #Parent node

def is_obstacle(x,y):
    """
    Function to check if the coordinate is in obstacle list
    """
    
    ind=obs_coord(x,y)
    if(ind == 1):
        #print("On obstacle")
        return True
    else:
        ind1 = obs_coord(x+ROBOT_RADIUS,y)
        ind2 = obs_coord(x,y+ROBOT_RADIUS)
        ind3 = obs_coord(x-ROBOT_RADIUS,y)
        ind4 = obs_coord(x,y-ROBOT_RADIUS)
        if(ind1 or ind2 or ind3 or ind4 == 1):
            return True
        else:
            return False

def is_valid_node(node):
    """ 
    Function that checks if a given node is valid or not
    """
    if(node.state[0]> MAP_WIDTH or node.state[1]>MAP_HEIGHT):
        #print(node.state)
        return False
    else:
        if(is_obstacle(node.state[0],node.state[1])):
            #print(node.state)
            return False
        return True

def generate_random_node(goal,rate):
    """
    Function that is used to generate a random node.
    """
    if np.random.random() > rate:   #The random node generation depends on the sample rate. If rate is really less, more random nodes will be generated.
        sample = Node()
        sample.state = [np.random.uniform((0 + ROBOT_RADIUS),(MAP_WIDTH - ROBOT_RADIUS)),
                        np.random.uniform((0 + ROBOT_RADIUS),(MAP_HEIGHT - ROBOT_RADIUS))]
        return sample
    return goal                                 

def node_in_tree(list,node):
    """
    Function that returns the node in the tree that is closest to the newly generated random node 
    """
    return list[int(np.argmin([math.hypot(nd.state[0] - node.state[0], nd.state[1] - node.state[1])
                                        for nd in list]))]

def check_collision(node1, node2):
        """
        Function to check if the path formed between two nodes, lies on an obstacle
        """
        x1, y1 = node1.state[0], node1.state[1] #Getting the coordinates of nodes
        x2, y2 = node2.state[0], node2.state[1]

        dx = math.ceil(x2 - x1)
        dy = math.ceil(y2 - y1)
        
        steps = 15
        
        x_step = dx // steps
        y_step = dy // steps

        # Check for collision with each point on the line segment
        for i in range(int(steps) + 1):

            x = math.ceil(x1 + i * x_step)
            y = math.ceil(y1 + i * y_step)

            # Check if the point collides with any obstacles
            dummy = Node()
            dummy.state = [x,y]
            if not is_valid_node(dummy):
                return True

        return False  # No collision

def node_new(node,rand_node):
    """
    Function that gives a new node along the direction of the newly generated node
    """
    coords = check_collision(node,rand_node)
    if(coords == False):
        dx = rand_node.state[0] - node.state[0]
        dy = rand_node.state[1] - node.state[1]
        dist = math.hypot(dx,dy)
        angle = math.atan2(dy,dx)
        min_dist = min(step_length,dist) #Check for step lenght
        new = Node()
        new.state = [node.state[0] + min_dist*math.cos(angle),node.state[1] + min_dist*math.sin(angle)]
        new.parent = node
        return new
    else:
        #print("Bad node")
        return None

def check_same(node1,node2):
    """
    Function to check if two nodes are the same
    """
    x = node1.state[0] - node2.state[0]
    y = node1.state[1] - node2.state[1]
    if math.hypot(x,y) == 0:
        return True
    return False

def set_parent(node1,node2):
    """
    Functon that sets one node as parent to other
    """
    new_node = Node()
    new_node.state = [node2.state[0],node2.state[1]]
    new_node.parent = node1
    return new_node

def path_gen(new_node_fwd, new_node_bwd):
    """
    Function that generates the path from the two trees
    """
    path = []
    path_fwd = []
    path_bwd = []
    path_fwd.append(new_node_fwd)
    curr_node = new_node_fwd 
    while curr_node.parent is not None:
        curr_node = curr_node.parent
        path_fwd.append(curr_node)
    path_bwd.append(new_node_bwd)
    curr_node = new_node_bwd
    while curr_node.parent is not None:
        curr_node = curr_node.parent
        path_bwd.append(curr_node)
    path = list(list(reversed(path_fwd)) + path_bwd)
    print("Path:")
    for any in path:
        print(any.state)
    return path

def visualize(fwd,bwd,path):
    """
    Function to visualize the path
    """
    pygame.init()

        # Set the window dimensions
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 200

    # Create the Pygame window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Obstacle Course")

    # Define the colors
    BACKGROUND_COLOR = pygame.Color("red")
    OBSTACLE_COLOR = pygame.Color("black")
    CLEARANCE_COLOR = pygame.Color("white")
    VISITED_COLOR = pygame.Color("green")
    PATH_COLOR = pygame.Color("blue")
    PIXEL_COLOR = pygame.Color("yellow")

    # Create the surface for the obstacle course
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    # pygame.display.flip()

    # Fill the surface with the background color
    surface.fill(BACKGROUND_COLOR)
    pygame.draw.rect(surface, CLEARANCE_COLOR, (0,0,5,200))
    pygame.draw.rect(surface, CLEARANCE_COLOR, (595,0,5,200))
    pygame.draw.rect(surface, CLEARANCE_COLOR, (0,0,600,5))
    pygame.draw.rect(surface, CLEARANCE_COLOR, (0,195,600,5))
    pygame.draw.rect(surface, CLEARANCE_COLOR, pygame.Rect(250-5, 70-5, 15+10, 125+10))
    pygame.draw.rect(surface, CLEARANCE_COLOR, pygame.Rect(150-5, 5-5, 15+10, 125+10))
    pygame.draw.circle(surface,CLEARANCE_COLOR,(400,90),55)
    # obs.append(pygame.draw.polygon(surface,color1,Trianlge1))


    #initialize Shapes
    
    (pygame.draw.rect(surface, OBSTACLE_COLOR, pygame.Rect(250, 70, 15, 125)))
    (pygame.draw.rect(surface, OBSTACLE_COLOR, pygame.Rect(150, 5, 15, 125)))
    (pygame.draw.circle(surface,OBSTACLE_COLOR,(400,90),50))

    len1,len2 = len(fwd),len(bwd)
    for k in range(max(len1,len2)):
        if k < len1:
            if fwd[k].parent:
                pygame.draw.line(surface,VISITED_COLOR,(fwd[k].state[0],fwd[k].state[1]),(fwd[k].parent.state[0],fwd[k].parent.state[1]),2)
        if k < len2:
            if bwd[k].parent:
                pygame.draw.line(surface,VISITED_COLOR,(bwd[k].state[0],bwd[k].state[1]),(bwd[k].parent.state[0],bwd[k].parent.state[1]),2)

        window.blit(surface,(0,0))
        pygame.time.wait(100)
            # pygame.display.flip()
        pygame.display.update()
    
    for idx,every in enumerate(path):
        if(every.parent is not None):
            pygame.draw.line(surface,PATH_COLOR,(every.parent.state[0],every.parent.state[1]),(every.state[0],every.state[1]),2)
            window.blit(surface, (0, 0))
     #Update the Pygame window display
            pygame.display.update()
    
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


    # Quit Pygame
    pygame.quit()

def rrt(goal,forward_visited,backward_visited):
    """
    Fucntion that runs the RRT algorithm
    """
    goal_flag = 0
    random_node = generate_random_node(goal,goal_sample_rate) #Generate ranom node
    node_near_in_tree_fwd = node_in_tree(forward_visited,random_node) #Finding the node in tree that is closest to the newly generated node
    new_node_fwd = node_new(node_near_in_tree_fwd,random_node) #Create a node along that direction

    if new_node_fwd is not None:
        forward_visited.append(new_node_fwd)    #Added to the forward tree
        node_near_in_tree_bwd = node_in_tree(backward_visited,new_node_fwd) # Finding node in the backward tree that is closest to the newly generated node in forward tree
        new_node_bwd = node_new(node_near_in_tree_bwd,new_node_fwd) #Creating a new node in that direction
        #print("Added to forward tree")

        if new_node_bwd is not None:
            #print(new_node_bwd.state)
            backward_visited.append(new_node_bwd) #Adding node to tree
            while True: #Repeating the same process from backward tree till the trees are connected or till a collision is detected
                new_node_bwd2 = node_new(new_node_bwd,new_node_fwd)
                if new_node_bwd2 is not None:
                    backward_visited.append(new_node_bwd2)
                    #print("Added to reverse tree")
                    new_node_bwd = set_parent(new_node_bwd,new_node_bwd2)
                else:
                    break
                if check_same(new_node_bwd2,new_node_fwd):
                    goal_flag = 1
                    print("Found path")
                    return path_gen(new_node_fwd,new_node_bwd),forward_visited,backward_visited
                
        if(len(backward_visited)<len(forward_visited)):
            new_list = backward_visited                     #Swap trees so that the other side is explored more
            backward_visited = forward_visited
            forward_visited = new_list
        
    if goal_flag == 0:
        #print("here")
        return(rrt(goal,forward_visited,backward_visited))

def get_startcoord_input(): #function to get start coordinates from user
    flag = False
    x = int(input("Enter x-ccordinate of start position:"))
    y = int(input("Enter y coordinate of start position:"))
    y = 200-y
    if(x<0 or x>=600 or y<0 or y>=250):
        print("Start coordinates out of bounds, Please enter x and y coordinates again")
        return [flag]
    elif (is_obstacle(x,y)):
        print("Start coordinates on an obstacle, Please enter x and y coordinates again")
        return [flag]
    else:
        return [True,x,y]
    
def get_goalcoord_input(): #Function to get goal coordinates from user
    flag = False
    xg = int(input("Enter x-ccordinate of goal position:"))
    yg = int(input("Enter y coordinate of goal position:"))
    yg = 200-yg
    if(xg<0 or xg>=600 or yg<0 or yg>=250):
        print("Goal coordinates out of bounds, Please enter x and y coordinates again")
        return [flag]
    elif(is_obstacle(xg,yg)):
        print("goal coordinates on an obstacle, Please enter x and y coordinates again")
        return [flag]
    else:
        return [True,xg,yg]
    
if __name__ == "__main__":
    forward_visited = []    #Tree from start node
    backward_visited = []   #Tree from goal node
    start = Node()
    goal = Node()
    a = True
    start_input = []
    while(a not in start_input):
        start_input = get_startcoord_input()    
    start.state  = [start_input[1],start_input[2]]
    goal_input = []
    while(a not in goal_input):
        goal_input = get_goalcoord_input()
    goal.state = [goal_input[1],goal_input[2]]
    start.parent = None
    goal.parent = None
    forward_visited.append(start)
    backward_visited.append(goal)
    print("RRT:")
    path,forward_visited,backward_visited = rrt(goal,forward_visited,backward_visited)
    visualize(forward_visited,backward_visited,path)