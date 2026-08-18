#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped, Quaternion
from nav2_msgs.action import NavigateToPose


class WarehouseNavigationNode(Node):

    def __init__(self):
        super().__init__('warehouse_navigation_node')

        self.declare_parameter('frame_id', 'map')
        self.declare_parameter('waypoints', [
            2.0, 1.0, 0.0,
            4.0, 1.0, 0.0,
            4.0, 3.0, 1.57,
            1.0, 3.0, 3.14
        ])

        self.frame_id = self.get_parameter(
            'frame_id'
        ).get_parameter_value().string_value

        waypoint_values = self.get_parameter(
            'waypoints'
        ).get_parameter_value().double_array_value

        if len(waypoint_values) % 3 != 0:
            self.get_logger().error(
                'Waypoints parameter must contain '
                'groups of 3 values: x, y, yaw'
            )

            raise ValueError(
                'Invalid waypoint configuration'
            )

        self.waypoints = []

        for i in range(0, len(waypoint_values), 3):
            x = waypoint_values[i]
            y = waypoint_values[i + 1]
            yaw = waypoint_values[i + 2]

            self.waypoints.append((x, y, yaw))

        self.current_waypoint_index = 0
        self.goal_handle = None
        self.goal_active = False


        self.nav_to_pose_client = ActionClient(
            self,
            NavigateToPose,
            '/navigate_to_pose'
        )

        self.get_logger().info(
            'warehouse_navigation_node started'
        )

        self.get_logger().info(
            f'Number of waypoints: {len(self.waypoints)}'
        )

        # Wait for Nav2 action server
        self.wait_for_nav2_server()



    def wait_for_nav2_server(self):

        self.get_logger().info(
            'Waiting for Nav2 /navigate_to_pose action server...'
        )

        self.nav_to_pose_client.wait_for_server()

        self.get_logger().info(
            'Nav2 /navigate_to_pose action server available'
        )

        self.send_next_waypoint()


    def quaternion_from_yaw(self, yaw):

        q = Quaternion()

        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)

        return q


    def create_goal(self, x, y, yaw):

        goal_pose = PoseStamped()

        goal_pose.header.frame_id = self.frame_id

        # Timestamp is generated using ROS time.
        goal_pose.header.stamp = self.get_clock().now().to_msg()

        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.position.z = 0.0

        goal_pose.pose.orientation = self.quaternion_from_yaw(yaw)

        return goal_pose


    def send_next_waypoint(self):

        # Check if all waypoints are completed

        if self.current_waypoint_index >= len(self.waypoints):


            self.get_logger().info(
                'All warehouse waypoints completed'
            )

            self.get_logger().info(
                'Navigation mission finished.'
            )

          

            return

        x, y, yaw = self.waypoints[
            self.current_waypoint_index
        ]

        self.get_logger().info(
            f'Sending waypoint '
            f'{self.current_waypoint_index + 1}/'
            f'{len(self.waypoints)}'
        )

        self.get_logger().info(
            f'Position: x={x:.2f}, y={y:.2f}, yaw={yaw:.2f}'
        )

        goal_msg = NavigateToPose.Goal()

        goal_msg.pose = self.create_goal(
            x,
            y,
            yaw
        )

        self.goal_active = True

        send_goal_future = self.nav_to_pose_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        send_goal_future.add_done_callback(
            self.goal_response_callback
        )


    def goal_response_callback(self, future):

        try:

            self.goal_handle = future.result()

        except Exception as e:

            self.get_logger().error(
                f'Failed to send navigation goal: {e}'
            )

            self.goal_active = False

            return


        if not self.goal_handle.accepted:

            self.get_logger().error(
                f'Waypoint '
                f'{self.current_waypoint_index + 1} '
                f'was rejected by Nav2'
            )

            self.goal_active = False

            return


        self.get_logger().info(
            f'Waypoint '
            f'{self.current_waypoint_index + 1} '
            f'accepted by Nav2'
        )



        result_future = self.goal_handle.get_result_async()

        result_future.add_done_callback(
            self.navigation_result_callback
        )



    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback


        try:

            distance_remaining = feedback.distance_remaining

            self.get_logger().info(
                f'Waypoint '
                f'{self.current_waypoint_index + 1}: '
                f'distance remaining = '
                f'{distance_remaining:.2f} m',
                throttle_duration_sec=2.0
            )

        except AttributeError:



            pass


    def navigation_result_callback(self, future):

        self.goal_active = False

        try:

            result = future.result()

        except Exception as e:

            self.get_logger().error(
                f'Error while receiving navigation result: {e}'
            )

            return

        status = result.status


        if status == GoalStatus.STATUS_SUCCEEDED:

            self.get_logger().info(
                f'Waypoint '
                f'{self.current_waypoint_index + 1} '
                f'reached successfully!'
            )

            self.current_waypoint_index += 1


            self.send_next_waypoint()


        elif status == GoalStatus.STATUS_CANCELED:

            self.get_logger().warn(
                f'Navigation to waypoint '
                f'{self.current_waypoint_index + 1} '
                f'was cancelled.'
            )


        elif status == GoalStatus.STATUS_ABORTED:

            self.get_logger().error(
                f'Navigation to waypoint '
                f'{self.current_waypoint_index + 1} '
                f'failed/aborted.'
            )

            self.get_logger().error(
                'Navigation mission stopped.'
            )

        else:

            self.get_logger().warn(
                f'Navigation finished with status: {status}'
            )


def main(args=None):

    rclpy.init(args=args)

    node = WarehouseNavigationNode()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        node.get_logger().info(
            'warehouse_navigation_node stopped.'
        )

    finally:

        node.destroy_node()

        rclpy.shutdown()


if __name__ == '__main__':
    main()