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

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
      print e

    #TODO Insert Image Processing Stuff Here

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError, e:
      print e


#TODO Calibration

class ball_follower:
  r = rospy.Rate(10)
  def __init__(self):
    self.move_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    self.move_sub  = rospy.Subscriber('PLACE HOLDER JEEZ AH', TYPE, coordinate_to_action)
    self.lin_vel = 0
    self.ang_vel = 0
  def coordinate_to_action(self, msg):
    #rows, cols, circle_rad
    y_transform = frame_height/2 - y
    x_transform = frame_width/2 - x
    angle_diff = math.tan(x/depth)
    twist = Twist()

    lin_proportion = 0.0015*depth
    twist.linear = Vector3(lin_proportion, 0, 0)

    turn_proportion = 0.0015*(angle_diff)
    twist.angular = Vector3(0, 0, turn_proportion)

    self.move_pub.publish(twist.linear, twist.angular)


def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"

if __name__ == '__main__':
    main(sys.argv)