 AUTONOMOUS MOBILE ROBOT USING ROS2 AND NAV2
This package is created for simulating autonomous navigation of a simple mobile robot inside a simulated warehouse environment.
The overall structure of the workspace is as follows
.
├── README.md
└── warehouse_robot
    ├── config
    │   ├── bridge_config.yaml
    │   ├── controllers.yaml
    │   ├── mapping.rviz
    │   ├── nav2_params.yaml
    │   ├── nav.rviz
    │   ├── sim.rviz
    │   └── warehouse_navigation.yaml
    ├── description
    │   ├── urdf_backup.urdf
    │   └── warehouse_bot.urdf
    ├── launch
    │   ├── mapping.launch.py
    │   ├── nav.launch.py
    │   ├── sim.launch.py
    │   └── warehouse_navigation.launch.py
    ├── maps
    │   ├── warehouse.pgm
    │   └── warehouse.yaml
    ├── package.xml
    ├── resource
    │   └── warehouse_robot
    ├── setup.cfg
    ├── setup.py
    ├── test
    │   ├── test_copyright.py
    │   ├── test_flake8.py
    │   └── test_pep257.py
    ├── warehouse_robot
    │   ├── __init__.py
    │   └── warehouse_navigation_node.py
    └── world
        ├── sim.sdf
        └── tugbot_warehouse
            ├── simulation.sdf
            └── thumbnails
                ├── 1.png
                ├── 2.png
                ├── 3.png
                └── 4.png
The package contains the Urdf for a simple differential drive mobile robot , which is equipped with a 360 degree 2d lidar and the launch files for running mapping using the simulated robot in simulated enviroments using slam toolbox, starting navigation simulation using the map made using slam toolbox and another launch file for launching a custom node which automatically sends a set of predefined waypoints in the map created one by one so that the user doesnot want to manually send waypoints. Currently there are 4 predefined waypoints added in the related yaml file , but the node is capable of handling more than 4 predefined waypoints if required.

The command for launching the Gazebo, urdf , robot state and joint state publishers are 
ros2 launch warehouse_robot sim.launch.py

The command for launching the mapping process is 
ros2 launch warehouse_robot mapping.launch.py

The command for launching the navigation stack (without custom node) is
ros2 launch warehouse_robot nav.launch.py

The command to launch the custom node for sending predefined navigation goals is
ros2 launch warehouse_robot warehouse_navigation.launch.py
