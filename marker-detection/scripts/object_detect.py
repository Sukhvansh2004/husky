#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy
import cv2
import numpy as np
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError

class ObjectDetector:
    def __init__(self):
        self.image_pub = rospy.Publisher("object_detection/image", Image, queue_size=10)
        self.object_pub = rospy.Publisher("object_detection/pose", PoseStamped, queue_size=10)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/realsense/color/image_raw", Image, self.image_callback)
        self.camera_info_sub = rospy.Subscriber("/realsense/color/camera_info", CameraInfo, self.camera_info_callback)
        self.distortion_coefficients = None
        self.matrix_coefficients = None

    def camera_info_callback(self, data):
        # Extract camera calibration parameters
        self.distortion_coefficients = data.D
        self.matrix_coefficients = data.K

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        # Implement object detection here
        detected_objects = self.detect_objects(cv_image)

        # Publish detected objects
        for obj in detected_objects:
            self.publish_object(obj)

        # Publish annotated image (optional)
        annotated_image = self.annotate_image(cv_image, detected_objects)
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(annotated_image, "bgr8"))
        except CvBridgeError as e:
            print(e)

    def detect_objects(self, cv_image):
        # Load pre-trained MobileNet SSD model
        model_path = "MobileNetSSD_deploy.caffemodel"
        prototxt_path = "MobileNetSSD_deploy.prototxt.txt"
        net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

        # Define classes for COCO dataset
        classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", 
                "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

        # Resize image and preprocess for inference
        blob = cv2.dnn.blobFromImage(cv_image, 0.007843, (300, 300), 127.5)

        # Set input and perform forward pass
        net.setInput(blob)
        detections = net.forward()

        detected_objects = []

        # Loop over the detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            # Filter out weak detections by confidence threshold
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])

                # Check if the detected class is a water bottle or a hammer (class IDs: 6 and 15 respectively)
                if class_id in [6, 15]:
                    # Extract bounding box coordinates
                    box = detections[0, 0, i, 3:7] * np.array([cv_image.shape[1], cv_image.shape[0], cv_image.shape[1], cv_image.shape[0]])
                    (startX, startY, endX, endY) = box.astype("int")

                    # Extract object position (center of the bounding box)
                    obj_x = (startX + endX) / 2
                    obj_y = (startY + endY) / 2
                    obj_z = 0  # Assuming 2D detection

                    # Create PoseStamped message for the detected object
                    obj_pose = PoseStamped()
                    obj_pose.header.frame_id = "camera_realsense_link"  # Adjust frame ID according to your setup
                    obj_pose.pose.position.x = obj_x
                    obj_pose.pose.position.y = obj_y
                    obj_pose.pose.position.z = obj_z
                    obj_pose.pose.orientation.w = 1.0  # Assuming no rotation

                    # Append the detected object pose to the list
                    detected_objects.append(obj_pose)

        return detected_objects

    def publish_object(self, obj_pose):
        # Publish the pose of a detected object
        self.object_pub.publish(obj_pose)

    def annotate_image(self, cv_image, detected_objects):
        # Annotate the image with bounding boxes or other visual indicators for detected objects
        # Return the annotated image
        annotated_image = cv_image.copy()

        # Example: Draw bounding boxes
        for obj in detected_objects:
            bbox = obj.bbox
            cv2.rectangle(annotated_image, (bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax), (0, 255, 0), 2)

        return annotated_image

def main(args):
    rospy.init_node('object_detector_node', anonymous=True)
    object_detector = ObjectDetector()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
