#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node

def get_launch_description():
    
    description_pkg_name = 'omnilogix_description'
    description_pkg_share = get_package_share_directory(description_pkg_name)
    
    controller_pkg_name = 'omnilogix_controller'
    controller_pkg_share = get_package_share_directory(controller_pkg_name)

    use_sim_time = LaunchConfiguration('use_sim_time')
    
    xacro_file = os.path.joint(description_pkg_share, 'urdf', 'kuka.urdf.xacro')
    
    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )
    
    rsp_node = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        parameters = [{'robot_description': robot_description,
                       'use_sim_time': use_sim_time}]
    )