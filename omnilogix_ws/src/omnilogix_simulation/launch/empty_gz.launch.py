#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument
)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    
    sim_pkg = 'omnilogix_simulation'
    sim_pkg_share = get_package_share_directory(sim_pkg)
    
    gz_pkg = 'ros_gz_sim'
    gz_pkg_share = get_package_share_directory(gz_pkg)
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    world_file = os.path.join(sim_pkg_share, 'worlds', 'empty_world.sdf')
    bridge_file = os.path.join(sim_pkg_share, 'config', 'bridge.yaml')
    
    gz_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_pkg_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments = {
            'gz_args': f'{world_file} -r -v1'
        }.items()
    )
    
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[ {'config_file': bridge_file}],
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'true',
            description = 'use_sim_time'
        ),
        gz_node,
        bridge_node
    ])
    