import sys
import rospy
import tf
from rrt_connect_661 import *
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf
import math
from tf import transformations
import roslaunch
import uuid

x = 0.0
y = 0.0 
theta = 0.0

def newOdom(msg):
    global x      #Odometry callback funtction
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = transformations.euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  #Getting yaw 

def move_tbot3(veocity_publisher,path):

    speed = Twist()

    r = rospy.Rate(4)
    n = len(path[2::3]) #Number of points
    print(n)
    i = 0
    for node in path[2::3]: #For each node in the path
        print("i=",i)    
        target_xpos = node.state[0]
        target_ypos = node.state[1]
        print("target_x = ",target_xpos)
        print("target_y = ",target_ypos)
        while True:
            angle_to_goal = math.atan2(target_ypos-y, target_xpos-x)  #Angle between robot's current orientation and target orientation
            dist = math.sqrt((target_xpos-x)**2 + (target_ypos-y)**2) #Distance between current position and target position
            if(dist<0.05):
                
                speed.linear.x = 0.0
                speed.angular.z = 0.0
                veocity_publisher.publish(speed)
                print("reached target")           
                print("x = ",target_xpos)
                print("y = ",target_ypos)
                print("x_robot = ",x)
                print("y_robot = ",y)
                break
            else:
                if abs(math.atan2(target_ypos-y, target_xpos-x) - theta) > 0.2:
                    speed.linear.x = 0.0
                    speed.angular.z = (math.atan2(target_ypos-y, target_xpos-x)-theta)*0.5  #Publishing angular and linear velocities proportional to the distance and orientation
                else:
                    speed.angular.z = 0.0
                    speed.linear.x = math.sqrt((target_xpos-x)**2 + (target_ypos-y)**2)*0.5
            veocity_publisher.publish(speed)
            r.sleep()
            if i == n-1 and (math.sqrt((target_xpos-x)**2 + (target_ypos-y)**2)<0.08):
               print("dist to goal:", math.sqrt((target_xpos-x)**2 + (target_ypos-y)**2))  #Last point
               speed.linear.x =0
               speed.angular.z = 0
               veocity_publisher.publish(speed)
               print("Goal reached")
               exit()
        i = i+1    

   

def main(args):
  forward_visited = []
  backward_visited = [] 
  rospy.init_node('controller')     #Initializing node
  velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10) #creating velocity publisher
  odom_sub = rospy.Subscriber('/odom', Odometry, newOdom)  #Odometry subscriber
  x_s, y_s = 50, 100 #Starting point
  x_g, y_g = 550, 30 #Goal
  start = Node()
  start.state = [x_s,y_s]
  start.parent = None
  goal = Node()
  goal.state = [x_g,200-y_g]    #For pygame, the y coordinate starts from top left.
  goal.parent = None
  forward_visited.append(start)
  backward_visited.append(goal)  
  path,_,_ = rrt(goal,forward_visited,backward_visited) #Getting path after performing rrtconnect
  #visualize(forward_visited,backward_visited,path)

  #print(traverse_list)
  for node in path: 
    node.state[0] = node.state[0]/100.0-0.5     #Transforming coordinates from -d world to gazebo world
    node.state[1] = (200-node.state[1])/100.0-1

  #print(traverse_list)
   
#   print((traverse_list[2][1] - y_pose)/((traverse_list[2][0] - x_pose) + 1e0-7))
  while (not rospy.is_shutdown()):

    try:

        move_tbot3(velocity_publisher, path)


    except KeyboardInterrupt:
        print("Shutting down")
# Shutdown the launch file 

if __name__ == '__main__':
    main(sys.argv)
