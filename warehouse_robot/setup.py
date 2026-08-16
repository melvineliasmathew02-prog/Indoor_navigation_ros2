from setuptools import find_packages, setup

package_name = 'warehouse_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/sim.launch.py','launch/mapping.launch.py','launch/nav.launch.py']),
        ('share/' + package_name + '/description', ['description/warehouse_bot.urdf']),
        ('share/' + package_name + '/config', ['config/controllers.yaml', 'config/bridge_config.yaml','config/sim.rviz','config/nav2_params.yaml','config/nav.rviz']),
        ('share/' + package_name + '/maps', ['maps/warehouse.yaml','maps/warehouse.pgm']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='melvin',
    maintainer_email='melvin@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
