#!/usr/bin/env python3

import rosbag
import os
import argparse
import open3d as o3d
from sensor_msgs.point_cloud2 import read_points


parser = argparse.ArgumentParser(description='Extract point cloud from a ROS bag file')
parser.add_argument('bag_file', metavar='BAG_FILE', type=str, help='dolly-104.bag')
parser.add_argument('-t', '--topic', metavar='TOPIC', type=str, default='/camera/points',
                    help='Name of topic to extract point cloud from (default: %(default)s)')
parser.add_argument('-o', '--output', metavar='OUTPUT_DIR', type=str, default='/rosbag_pointcloud',
                    help='Path to output directory (default: %(default)s)')
parser.add_argument('--start_time', type=float,default='0',
                    help='Start time (in seconds) to extract pointclouds from')
parser.add_argument('--end_time', type=float,default='99999999999999999',
                    help='End time (in seconds) to extract pointclouds to')
args = parser.parse_args()

# Create output directory if it doesn't exist
if not os.path.exists(args.output):
    os.makedirs(args.output)

# Open the ROS bag file and read the point cloud messages
with rosbag.Bag(args.bag_file, 'r') as bag:
    for topic, msg, t in bag.read_messages(topics=args.topic):
        # Check if the current message timestamp is within the time range
        if (args.start_time is None or t.to_sec() >= args.start_time) and \
            (args.end_time is None or t.to_sec() <= args.end_time):
            # Convert PointCloud2 message to Open3D PointCloud
            points = list(read_points(msg))
            pc = o3d.geometry.PointCloud()
            pc.points = o3d.utility.Vector3dVector(points)
            # Save PointCloud to PCD file
            output_file = os.path.join(args.output, f'{t.to_nsec()}.pcd')
            o3d.io.write_point_cloud(output_file, pc)
