#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time

class TrajectoryTest(Node):

    def __init__(self):
        super().__init__('trajectory_test')
        topic_name = "/dofbot_trajectory_controller/joint_trajectory"
        self.trajectory_publisher = self.create_publisher(JointTrajectory, topic_name, 10)
        self.joints = ['arm_joint_01', 'arm_joint_02', 'arm_joint_03', 'arm_joint_04', 'arm_joint_05', 'grip_joint', 
                       'rfinger_joint_01',
                       'rfinger_joint_02',
                       'lfinger_grip_joint_01',
                       'lfinger_grip_joint_02',
                       'lfinger_grip_joint_03']

        self.goal_positions_list = [
                            [1.11, 0.83, -0.41, -1.55, -1.56, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [0.34, 0.82, 0.15, 0.94, 0.57,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [0.67, -1.23, 1.04, -0.56, 1.12,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00], 
                            [-1.45, 1.01, -0.89, 1.30, -1.57,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [1.22, -1.15, 1.39, -0.98, 0.47,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [-0.78, 1.33, -1.03, 0.99, -1.50,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [0.23, -1.45, 1.56, -1.01, 0.89,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [0.32, -1.13, -0.18, -0.42, 0.55,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [0.27, 0.77, 0.49, 0.11, 0.89,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [1.55, -0.77, 0.22, -0.66, 1.49,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [0.58, -0.34, 1.55, -0.45, 0.67,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00], 
                            [1.20, -0.67, 1.41, -0.59, 1.18,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                            [1.43, -0.55, 0.67, -1.23, 1.56,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00]                       
                            ]

        self.current_goal_index = 0
        self.trajectory_active = False
        self.timer = self.create_timer(3, self.timer_callback)
        self.get_logger().info('Controller is running and publishing to topic: {}'.format(topic_name))

    def timer_callback(self):
        if not self.trajectory_active and self.current_goal_index < len(self.goal_positions_list):
            self.publish_trajectory(self.goal_positions_list[self.current_goal_index])
            self.current_goal_index += 1
            self.trajectory_active = True

    def publish_trajectory(self, goal_positions):
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = self.joints
        point = JointTrajectoryPoint()
        point.positions = goal_positions
        point.time_from_start = Duration(sec=2)
        trajectory_msg.points.append(point)
        self.trajectory_publisher.publish(trajectory_msg)
        self.get_logger().info('Published trajectory: {}'.format(goal_positions))
        self.create_timer(3, self.trajectory_complete_callback)  # Wait for the trajectory to complete

    def trajectory_complete_callback(self):
        self.get_logger().info('Completed trajectory {}'.format(self.current_goal_index))
        time.sleep(2)
        self.trajectory_active = False

def main(args=None):
    rclpy.init(args=args)
    trajectory_publisher_node = TrajectoryTest()
    rclpy.spin(trajectory_publisher_node)
    trajectory_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()