#!/usr/bin/env python
import os
import rosbag
import cv2
from cv_bridge import CvBridge
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Extract images from a ROS bag file.')
parser.add_argument('bag_file', help='Path to the ROS bag file')
parser.add_argument('--topic', default='/camera/image_raw', help='ROS topic containing the images')
parser.add_argument('--output', default='./', help='Output directory for the extracted images')
parser.add_argument('--format', default='.png', help='Output image format (.png, .jpg)')
parser.add_argument('--start_time', type=float,default='0',
                    help='Start time (in seconds) to extract images from')
parser.add_argument('--end_time', type=float,default='99999999999999999',
                    help='End time (in seconds) to extract images to')
args = parser.parse_args()

# Create the output folder if it doesn't exist
if not os.path.exists(args.output):
    os.makedirs(args.output)

# Create a CvBridge object to convert ROS messages to OpenCV images
bridge = CvBridge()
# Open the bag file and iterate through the messages
with rosbag.Bag(args.bag_file, 'r') as bag:
    for topic, msg, t in bag.read_messages(topics=args.topic):
        # Check if the current message timestamp is within the time range
        if (args.start_time is None or t.to_sec() >= args.start_time) and \
                (args.end_time is None or t.to_sec() <= args.end_time):
            # Convert the ROS message to an OpenCV image
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

            # Save the OpenCV image as a file
            file_name = os.path.join(args.output, str(t) + args.format)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            cv2.imwrite(file_name, cv_image)