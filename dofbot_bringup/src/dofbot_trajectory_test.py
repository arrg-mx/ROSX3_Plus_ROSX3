#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time

class ArmTrajectoryTest(Node):

    def __init__(self):
        super().__init__('arm_trajectory_test')
        topic_name = "/dofbot_trajectory_controller/joint_trajectory"
        self.trajectory_publisher = self.create_publisher(JointTrajectory, topic_name, 10)
        self.joints = ['arm_joint_01', 'arm_joint_02', 'arm_joint_03', 'arm_joint_04', 'arm_joint_05']

        self.goal_positions_list = [
            [0.36, -1.08, -0.52, -0.59, 3.14],
            [-1.08, 0.15, 1.53, 0.47, -0.14],
            [1.07, 0.92, -1.38, -1.13, 1.25],
            [-1.21, 0.18, 1.34, 0.43, -0.41],
            [-0.95, 0.72, 0.21, -1.37, 3.14],
            [-1.21, -0.77, -1.55, 0.81, 0.11]
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
        self.create_timer(10, self.trajectory_complete_callback)  # Wait for the trajectory to complete

    def trajectory_complete_callback(self):
        self.get_logger().info('Completed trajectory {}'.format(self.current_goal_index))
        time.sleep(2)
        self.trajectory_active = False

def main(args=None):
    rclpy.init(args=args)
    trajectory_publisher_node = ArmTrajectoryTest()
    rclpy.spin(trajectory_publisher_node)
    trajectory_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
