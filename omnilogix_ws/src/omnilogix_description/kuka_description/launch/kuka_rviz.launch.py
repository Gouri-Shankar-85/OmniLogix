#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    
    pkg_name = 'kuka_description'
    pkg_share = get_package_share_directory(pkg_name)
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    urdf_file = os.path.join(pkg_share, 'urdf', 'kr16_2.urdf')
    
    with open(urdf_file, 'r') as urdf:
        robot_description = urdf.read()
        
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
            description = 'Use simulation clock time'
        ),
        rsp_node,
        jsp_gui_node
    ])