#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time

class GripperTrajectoryTest(Node):

    def __init__(self):
        super().__init__('gripper_trajectory_test')
        topic_name = "/dofbot_gripper_controller/joint_trajectory"
        self.trajectory_publisher = self.create_publisher(JointTrajectory, topic_name, 10)
        self.joints = ['grip_joint', 'rfinger_joint_01', 'rfinger_joint_02', 'lfinger_grip_joint_01', 'lfinger_grip_joint_02', 'lfinger_grip_joint_03']

        self.goal_positions_list = [
            [-1.54, 1.54, -1.54, 1.54, -1.54, 1.54],
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
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
    trajectory_publisher_node = GripperTrajectoryTest()
    rclpy.spin(trajectory_publisher_node)
    trajectory_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
