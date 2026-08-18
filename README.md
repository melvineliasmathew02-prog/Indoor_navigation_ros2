# AUTONOMOUS MOBILE ROBOT USING ROS2 AND NAV2

This package is created for simulating autonomous navigation of a simple mobile robot inside a simulated warehouse environment.

## Workspace Structure

The overall structure of the workspace is as follows:

```text
.
├── README.md
└── warehouse_robot
    ├── config
    │   ├── bridge_config.yaml
    │   ├── controllers.yaml
    │   ├── mapping.rviz
    │   ├── nav2_params.yaml
    │   ├── nav.rviz
    │   ├── sim.rviz
    │   └── warehouse_navigation.yaml
    ├── description
    │   ├── urdf_backup.urdf
    │   └── warehouse_bot.urdf
    ├── launch
    │   ├── mapping.launch.py
    │   ├── nav.launch.py
    │   ├── sim.launch.py
    │   └── warehouse_navigation.launch.py
    ├── maps
    │   ├── warehouse.pgm
    │   └── warehouse.yaml
    ├── package.xml
    ├── resource
    │   └── warehouse_robot
    ├── setup.cfg
    ├── setup.py
    ├── test
    │   ├── test_copyright.py
    │   ├── test_flake8.py
    │   └── test_pep257.py
    ├── warehouse_robot
    │   ├── __init__.py
    │   └── warehouse_navigation_node.py
    └── world
        ├── sim.sdf
        └── tugbot_warehouse
            ├── simulation.sdf
            └── thumbnails
                ├── 1.png
                ├── 2.png
                ├── 3.png
                └── 4.png
```

## Package Description

The package contains the URDF for a simple differential-drive mobile robot, which is equipped with a 360-degree 2D LiDAR.

It also contains the required launch files for running mapping using the simulated robot in a simulated warehouse environment using SLAM Toolbox.

The package provides the following functionality:

- Simulating a differential-drive mobile robot in a warehouse environment.
- Running SLAM Toolbox for mapping the simulated environment.
- Saving and using the generated map for autonomous navigation.
- Running the Nav2 navigation stack.
- Automatically sending predefined navigation waypoints using a custom ROS2 node.
- Sequentially navigating the robot through multiple predefined waypoints.

The custom navigation node automatically sends a set of predefined waypoints in the map, one by one. This means that the user does not need to manually send individual navigation goals.

Currently, there are **4 predefined waypoints** added in the related YAML configuration file. However, the custom navigation node is capable of handling more than 4 predefined waypoints if required.

## Launch Commands

### 1. Launch the Simulation

The following command launches Gazebo along with the URDF, robot state publisher, and joint state publisher:

```bash
ros2 launch warehouse_robot sim.launch.py
```

### 2. Launch the Mapping Process

The following command launches the mapping process using SLAM Toolbox:

```bash
ros2 launch warehouse_robot mapping.launch.py
```

### 3. Launch the Navigation Stack

The following command launches the Nav2 navigation stack without the custom navigation node:

```bash
ros2 launch warehouse_robot nav.launch.py
```

### 4. Launch the Custom Navigation Node

The following command launches the custom node for automatically sending predefined navigation goals:

```bash
ros2 launch warehouse_robot warehouse_navigation.launch.py
```

## Navigation Waypoints

Currently, the package contains **4 predefined navigation waypoints** in the related YAML configuration file.

The custom navigation node reads these predefined waypoints and sends them to the Nav2 navigation stack sequentially.

The node can also be configured to handle more than 4 predefined waypoints if required.

## Summary

This package provides a complete simulation environment for experimenting with autonomous mobile robot navigation using:

- ROS2
- Gazebo
- Nav2
- SLAM Toolbox
- URDF
- 2D LiDAR
- Differential-drive mobile robot
- Custom waypoint navigation

The robot can be simulated inside a warehouse environment, generate a map using SLAM Toolbox, use the generated map for autonomous navigation, and navigate through a sequence of predefined waypoints automatically.