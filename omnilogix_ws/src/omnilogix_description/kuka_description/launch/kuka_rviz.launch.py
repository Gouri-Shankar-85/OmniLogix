#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node, PushRosNamespace

def create_arm_group(kuka_id, xacro_path, use_sim_time):
    
    robot_description = ParameterValue(
        Command(['xacro ', xacro_path]),
        value_type=str
    )
    
    return GroupAction([
        PushRosNamespace(kuka_id),
        
        Node(
            package = 'robot_state_publisher',
            executable = 'robot_state_publisher',
            parameters = [{
                'robot_description': robot_description, 
                'use_sim_time': use_sim_time
            }],    
        ),
        
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            parameters = [{
                'robot_description': robot_description, 
                'use_sim_time': use_sim_time
            }],      
            output='screen'
        )   
    ])

def generate_launch_description():
    
    pkg_name = 'kuka_description'
    pkg_share = get_package_share_directory(pkg_name)
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    arms = ['kuka_1', 'kuka_2', 'kuka_3', 'kuka_4']
    
    arm_groups = [
        create_arm_group(
            kuka_id = arm,
            xacro_path = os.path.join(pkg_share, 'urdf', f'{arm}.urdf.xacro'),
            use_sim_time = use_sim_time
        )
        for arm in arms
    ]
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'false',
            description = 'If true: use simulation clock time'
        ),
        *arm_groups
    ])