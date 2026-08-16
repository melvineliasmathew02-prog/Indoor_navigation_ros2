import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    # ---------------------------------------------------------
    # Package paths
    # ---------------------------------------------------------

    pkg_warehouse_bot = get_package_share_directory('warehouse_robot')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    urdf_file = os.path.join(
        pkg_warehouse_bot, 'description', 'warehouse_bot.urdf'
    )

    # Path to bridge config file
    bridge_config_file = os.path.join(
        pkg_warehouse_bot, 'config', 'bridge_config.yaml'
    )

    # ---------------------------------------------------------
    # Read URDF
    # ---------------------------------------------------------

    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    # ---------------------------------------------------------
    # Gazebo Harmonic
    # ---------------------------------------------------------

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': '-r /home/melvin/ihub_ws/src/warehouse_robot/world/tugbot_warehouse/simulation.sdf'
        }.items(),
    )

    # ---------------------------------------------------------
    # ROS-GZ Bridge (Configured via YAML file)
    # ---------------------------------------------------------

    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_config_file}',
        ],
        output='screen',
        parameters=[{'use_sim_time': True}],
    )

    # ---------------------------------------------------------
    # Robot State Publisher
    # ---------------------------------------------------------

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description, 'use_sim_time': True}
        ],
    )

    # ---------------------------------------------------------
    # Spawn robot into Gazebo
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Joint State Broadcaster
    # ---------------------------------------------------------

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager',
        ],
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    # ---------------------------------------------------------
    # Differential Drive Controller
    # ---------------------------------------------------------

    diff_drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_controller',
            '--controller-manager',
            '/controller_manager',
        ],
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    rviz2 = Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
            arguments=['-d',os.path.join(pkg_warehouse_bot, 'config', 'mapping.rviz')]
        )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('slam_toolbox'),
                'launch',
                'online_async_launch.py'
            )
        )
    )
    # ---------------------------------------------------------
    # Launch everything
    # ---------------------------------------------------------

    return LaunchDescription([
        gazebo,
        clock_bridge,
        robot_state_publisher,
        spawn_robot,
        joint_state_broadcaster_spawner,
        diff_drive_controller_spawner,
        slam,
        rviz2,
    ])