import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    # ============================================================
    # Package directories
    # ============================================================

    pkg_warehouse_bot = get_package_share_directory('warehouse_robot')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # ============================================================
    # File paths
    # ============================================================

    urdf_file = os.path.join(
        pkg_warehouse_bot,
        'description',
        'warehouse_bot.urdf'
    )

    bridge_config_file = os.path.join(
        pkg_warehouse_bot,
        'config',
        'bridge_config.yaml'
    )

    nav2_params_file = os.path.join(
        pkg_warehouse_bot,
        'config',
        'nav2_params.yaml'
    )

    map_file = os.path.join(
        pkg_warehouse_bot,
        'maps',
        'warehouse.yaml'
    )

    rviz_config_file = os.path.join(
        pkg_warehouse_bot,
        'config',
        'nav.rviz'
    )

    # ============================================================
    # Read URDF
    # ============================================================

    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    # ============================================================
    # Gazebo
    # ============================================================

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_ros_gz_sim,
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args':
                '-r /home/melvin/ihub_ws/src/warehouse_robot/'
                'world/tugbot_warehouse/simulation.sdf'
        }.items(),
    )

    # ============================================================
    # ROS-Gazebo bridge
    # ============================================================

    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_config_file}',
        ],
        output='screen',
        parameters=[
            {'use_sim_time': True}
        ],
    )

    # ============================================================
    # Robot State Publisher
    # ============================================================

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': True
            }
        ],
    )

    # ============================================================
    # Spawn robot in Gazebo
    # ============================================================

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name',
            'warehouse_bot',

            '-topic',
            'robot_description',

            '-x',
            '0.0',

            '-y',
            '0.0',

            '-z',
            '0.2',
        ],
        output='screen',
    )

    # ============================================================
    # Joint State Broadcaster
    # ============================================================

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager',
        ],
        parameters=[
            {'use_sim_time': True}
        ],
        output='screen',
    )

    # ============================================================
    # Differential Drive Controller
    # ============================================================

    diff_drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_controller',
            '--controller-manager',
            '/controller_manager',
        ],
        parameters=[
            {'use_sim_time': True}
        ],
        output='screen',
    )

    # ============================================================
    # MAP SERVER
    #
    # Loads the previously generated map.
    # ============================================================

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[
            {
                'yaml_filename': map_file,
                'use_sim_time': True
            }
        ],
    )

    # ============================================================
    # AMCL
    #
    # Localizes the robot on the saved map using:
    #
    #   /scan
    #   /odom
    #
    # and publishes:
    #
    #   map -> odom
    # ============================================================

    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[
            nav2_params_file,
            {'use_sim_time': True}
        ],
    )

    # ============================================================
    # Planner Server
    #
    # Calculates the global path from robot to goal.
    # ============================================================

    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[
            nav2_params_file,
            {'use_sim_time': True}

        ],
    )

    # ============================================================
    # Controller Server
    #
    # Follows the planned path and generates /cmd_vel.
    # ============================================================

    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[
            nav2_params_file,
            {'use_sim_time': True }
        ],
        remappings=[
            ('/cmd_vel', '/diff_drive_controller/cmd_vel'),
        ],
    )

    # ============================================================
    # Behavior Server
    #
    # Handles recovery behaviors such as:
    #
    #   spin
    #   backup
    #   wait
    # ============================================================

    behavior_server = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[
            nav2_params_file,
            {'use_sim_time': True}
        ],
    )

    # ============================================================
    # BT Navigator
    #
    # Controls the overall navigation behavior tree.
    # ============================================================

    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[
            nav2_params_file,
            {'use_sim_time': True}
        ],
    )

    # ============================================================
    # Waypoint Follower
    #
    # Allows navigation through multiple goals.
    # ============================================================

    waypoint_follower = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[
            nav2_params_file,
            {'use_sim_time': True}
        ],
    )

    # ============================================================
    # Lifecycle Manager - Localization
    #
    # Manages:
    #
    #   map_server
    #   amcl
    # ============================================================

    lifecycle_localization = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[
            {
                'use_sim_time': True,
                'autostart': True,
                'node_names': [
                    'map_server',
                    'amcl'
                ]
            }
        ],
    )

    # ============================================================
    # Lifecycle Manager - Navigation
    #
    # Manages:
    #
    #   planner_server
    #   controller_server
    #   behavior_server
    #   bt_navigator
    #   waypoint_follower
    # ============================================================

    lifecycle_navigation = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[
            {
                'use_sim_time': True,
                'autostart': True,
                'node_names': [
                    'planner_server',
                    'controller_server',
                    'behavior_server',
                    'bt_navigator',
                    'waypoint_follower'
                ]
            }
        ],
    )

    # ============================================================
    # RViz2
    # ============================================================

    rviz2 = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        name='rviz2',
        arguments=[
            '-d',
            rviz_config_file
        ],
        parameters=[
            {'use_sim_time': True}
        ],
        output='screen'
    )

    # ============================================================
    # Launch Description
    # ============================================================

    return LaunchDescription([

        # Gazebo
        gazebo,

        # Gazebo <-> ROS bridge
        clock_bridge,

        # Robot
        robot_state_publisher,
        spawn_robot,

        # ros2_control
        joint_state_broadcaster_spawner,
        diff_drive_controller_spawner,

        # Navigation
        map_server,
        amcl,
        planner_server,
        controller_server,
        behavior_server,
        bt_navigator,
        waypoint_follower,

        # Lifecycle managers
        lifecycle_localization,
        lifecycle_navigation,

        # Visualization
        rviz2,
    ])