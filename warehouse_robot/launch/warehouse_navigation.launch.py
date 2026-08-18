from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    package_dir = get_package_share_directory(
        'warehouse_robot'
    )

    params_file = os.path.join(
        package_dir,
        'config',
        'warehouse_navigation.yaml'
    )

    navigation_node = Node(
        package='warehouse_robot',
        executable='warehouse_navigation_node',
        name='warehouse_navigation_node',
        output='screen',
        parameters=[
            params_file,
            {
                'use_sim_time': True
            }
        ]
    )

    return LaunchDescription([
        navigation_node
    ])