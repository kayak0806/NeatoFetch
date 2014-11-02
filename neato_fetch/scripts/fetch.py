#!/usr/bin/env python
import roslib
roslib.load_manifest('neato_fetch')
import rospkg
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist, Vector3

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("/processed_image",Image)
    self.ball_pub = rospy.Publisher("/ball_coords",Vector3)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/image_raw",Image,self.callback)
    self.circle_location = []

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
      print e

    #Image Processing
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 150)
    self.find_circles(edges,cv_image)


    # ball = self.circle_location[-1]
    # location = Vector3(ball[0],ball[1],ball[2])


    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
      # self.ball_pub.publish(location)
    except CvBridgeError, e:
      print e

  def find_circles(self,img_src, img_out):
    """Finds and plots circles using Hough Circle detection."""
    circles = cv2.HoughCircles(img_src, cv2.cv.CV_HOUGH_GRADIENT, 1, img_src.shape[0]/8, param1=10, param2=20, minRadius=10, maxRadius=20)

    if circles is not None:
      for c in circles[0,:]:
          # draw the outer circle
          cv2.circle(img_out,(c[0],c[1]),c[2],(0,255,0),2)
          # draw the center of the circle
          cv2.circle(img_out,(c[0],c[1]),2,(0,0,255),3)
          self.circle_location.append((c[0], c[1],c[2]))
          print (c[0],c[1],c[2])

"""
class ball_follower:
  r = rospy.Rate(10)
  def __init__(self):
    self.move_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    self.move_sub  = rospy.Subscriber('ball_coords', Vector3, coordinate_to_action)
    self.lin_vel = 0
    self.ang_vel = 0
    self.frame_height = 480
    self.frame_width = 640
  def coordinate_to_action(self, msg):
    y = self.move_sub[1]
    x = self.move_sub[0]
    r = self.move_sub[2]

    depth_proportion = 
    depth = r*depth_proportion
    y_transform = self.frame_height/2 - y
    x_transform = self.frame_width/2 - x
    angle_diff = math.tan(x/depth)

    twist = Twist()

    lin_proportion = 0.0015*depth
    twist.linear = Vector3(lin_proportion, 0, 0)

    turn_proportion = 0.0015*(angle_diff)
    twist.angular = Vector3(0, 0, turn_proportion)

    self.move_pub.publish(twist.linear, twist.angular)
"""

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  fido = ball_follower()
  rospy.init_node('ball_follower', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"

if __name__ == '__main__':
    main(sys.argv)