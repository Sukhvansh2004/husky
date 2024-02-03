#!/usr/bin/env python3
from __future__ import print_function

import sys
import rospy
import cv2
import tf
from geometry_msgs.msg import PoseStamped
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError

distortion_coefficients = []
matrix_coefficients = []
betweenPose = PoseStamped()
postPose = PoseStamped()
mode = "P"

class image_converter:
  
  def __init__(self):
    self.image_pub = rospy.Publisher("between_image",Image,queue_size=10)
    self.between_pub = rospy.Publisher("/move_base_simple/goal",PoseStamped,queue_size=1)
    self.bridge = CvBridge()
    self.calibrate_camera = rospy.Subscriber("/realsense/color/camera_info",CameraInfo,self.callbackCalibrate)
    self.image_sub = rospy.Subscriber("/realsense/color/image_raw",Image,self.callback)
    

  def callback(self,data):
    
    global distortion_coefficients
    global matrix_coefficients

    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    
    cv_image_gray = cv_image.copy()
    cv_image_gray = cv2.cvtColor(cv_image_gray, cv2.COLOR_BGR2GRAY )

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cv_image_gray = clahe.apply(cv_image_gray)

    cv_image_gray = cv2.medianBlur(cv_image_gray, 5) 


    
    height, width = cv_image.shape[:2]

    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()

    (corners, ids, rejected) = cv2.aruco.detectMarkers(cv_image_gray, arucoDict, parameters=arucoParams)

    positionX = 0
    positionY = 0
    positionZ = 0

    orientationX = 0
    orientationY = 0
    orientationZ = 0
    orientationW = 0

    if len(corners) > 0:
        for i in range(0, len(ids)):

          rvec, tvec, _= cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.2, matrix_coefficients,
                                                                       distortion_coefficients)


          cv2.aruco.drawDetectedMarkers(cv_image, corners) 
          cv2.aruco.drawAxis(cv_image, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.1)  
          rotation_matrix = np.array([[0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 1]],
                            dtype=float)
          rotation_matrix[:3, :3], _ = cv2.Rodrigues(rvec)

          quaternion = tf.transformations.quaternion_from_matrix(rotation_matrix)

          if mode == "P":  
            self.publishPostPose(tvec[0][0][0],tvec[0][0][1],tvec[0][0][2],quaternion[0],quaternion[1],quaternion[2],quaternion[3])

          else:
            positionX = tvec[0][0][0] + positionX
            positionY = tvec[0][0][1] + positionY
            positionZ = tvec[0][0][2] + positionZ

            orientationX = quaternion[0] + orientationX
            orientationY = quaternion[1] + orientationY
            orientationZ = quaternion[2] + orientationZ
            orientationW = quaternion[3] + orientationW


          # cv2.imshow("Image window", cv_image)

    if mode == "G":
      self.publishGatePose(corners, positionX,positionY,positionZ,orientationX,orientationY,orientationZ,orientationW)
      if len(corners)> 1:
        firstMarkerUpX = (corners[0][0][0][0] + corners[0][0][1][0]) / 2
        firstMarkerUpY = (corners[0][0][0][1] + corners[0][0][1][1]) / 2

        firstMarkerDownX = (corners[0][0][2][0] + corners[0][0][3][0]) / 2
        firstMarkerDownY= (corners[0][0][2][1] + corners[0][0][3][1]) / 2

        secondMarkerUpX = (corners[1][0][0][0] + corners[1][0][1][0]) / 2
        secondMarkerUpY = (corners[1][0][0][1] + corners[1][0][1][1]) / 2

        secondMarkerDownX = (corners[1][0][2][0] + corners[1][0][3][0]) / 2
        secondMarkerDownY= (corners[1][0][2][1] + corners[1][0][3][1]) / 2

        firstMarkerCenterX = (firstMarkerUpX +   firstMarkerDownX) / 2
        firstMarkerCenterY = (secondMarkerUpY +   firstMarkerDownY) / 2

        secondMarkerCenterX = (secondMarkerUpX +   secondMarkerDownX) / 2
        secondMarkerCenterY = ( secondMarkerUpY +   secondMarkerDownY) / 2

        cv2.circle(cv_image,(int((firstMarkerCenterX +secondMarkerCenterX) / 2), int((firstMarkerCenterY +secondMarkerCenterY) / 2)), 10, (0,0,255), -1)


    self.drawMarker(corners,ids,cv_image=cv_image)

  def publishPostPose(self,pX, pY,pZ, oX,oY,oZ, oW):
    global postPose
    postPose = PoseStamped()
    postPose.header.frame_id = "base_link"
    postPose.pose.position.x = pZ 
    postPose.pose.position.y = pX 
    postPose.pose.position.z = 0

    postPose.pose.orientation.x = 0
    postPose.pose.orientation.y = 0
    postPose.pose.orientation.z = oZ
    postPose.pose.orientation.w = oW 
            
    self.between_pub.publish(postPose)      

  def publishGatePose(self,corners, pX, pY,pZ, oX,oY,oZ, oW):
    if len(corners) > 1:
      global betweenPose
      betweenPose = PoseStamped()
      betweenPose.header.frame_id = "between_point"
      betweenPose.pose.position.x = pZ / 2
      betweenPose.pose.position.y = pX / 2
      betweenPose.pose.position.z = pY / 2

      betweenPose.pose.orientation.x = oX / 2
      betweenPose.pose.orientation.y = oY / 2
      betweenPose.pose.orientation.z = oZ / 2
      betweenPose.pose.orientation.w = oW / 2
      self.between_pub.publish(betweenPose)

  def drawMarker(self, corners, ids, cv_image):
    if len(corners) > 0:
      ids = ids.flatten()
      for (markerCorner, markerID) in zip(corners, ids):
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners

        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        cv2.line(cv_image, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(cv_image, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(cv_image, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(cv_image, bottomLeft, topLeft, (0, 255, 0), 2)
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(cv_image, (cX, cY), 4, (0, 0, 255), -1)
        cv2.putText(cv_image, str(markerID),
          (topLeft[0], topLeft[1] - 15),
          cv2.FONT_HERSHEY_SIMPLEX,
          1, (0, 255, 0), 2) 
    
 #   cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)
    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

  def callbackCalibrate(self,data):
      global distortion_coefficients
      global matrix_coefficients

      distortion_coefficients = []
      matrix_coefficients = []

      distortion_coefficients.append(data.D[0])
      distortion_coefficients.append(data.D[1])
      distortion_coefficients.append(data.D[2])
      distortion_coefficients.append(data.D[3])
      distortion_coefficients.append(data.D[4])
        
      matrix_coefficients.append([])
      matrix_coefficients[0].append(data.K[0])
      matrix_coefficients[0].append(data.K[1])
      matrix_coefficients[0].append(data.K[2])

      matrix_coefficients.append([])
      matrix_coefficients[1].append(data.K[3])
      matrix_coefficients[1].append(data.K[4])
      matrix_coefficients[1].append(data.K[5])

      matrix_coefficients.append([])
      matrix_coefficients[2].append(data.K[6])
      matrix_coefficients[2].append(data.K[7])
      matrix_coefficients[2].append(data.K[8])

      distortion_coefficients = np.array(distortion_coefficients)
      matrix_coefficients = np.array(matrix_coefficients)

      self.unsubscribe()
      
  def unsubscribe(self):
    self.calibrate_camera.unregister()

def main(args):
  global mode
  mode = args[1]
  rospy.init_node('image_converter', anonymous=True)
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
