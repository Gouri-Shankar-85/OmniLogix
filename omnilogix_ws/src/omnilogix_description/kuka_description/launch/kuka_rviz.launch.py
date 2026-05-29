#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node

def generate_launch_description():
    
    pkg_name = 'kuka_description'
    pkg_share = get_package_share_directory(pkg_name)
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    xacro_file = os.path.join(pkg_share, 'urdf', 'kuka.urdf.xacro')
    
    robot_description = ParameterValue(
        Command(['xacro', xacro_file]),
        value_type=str
    )
        
    rsp_node = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        parameters = [{'robot_description': robot_description, 
                       'use_sim_time': use_sim_time}],
        output = 'screen'
    )
    
    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        parameters = [{'robot_description': robot_description, 
                       'use_sim_time': use_sim_time}],      
        output='screen'
    )   
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'false',
            description = 'If true: use simulation clock time'
        ),
        rsp_node,
        jsp_gui_node
    ])