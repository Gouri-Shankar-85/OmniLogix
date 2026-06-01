#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction
)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    
    ctrl_pkg = 'omnilogix_controller'
    ctrl_pkg_share = get_package_share_directory(ctrl_pkg)
    
    sim_pkg = 'omnilogix_simulation'
    sim_pkg_share = get_package_share_directory(sim_pkg)
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    sim_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(sim_pkg_share, 'launch', 'empty_gz.launch.py')
        ),
        launch_arguments = {'use_sim_time': use_sim_time}.items()
    )
    
    kuka_arm_node = TimerAction(
        period = 10.0,
        actions = [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(ctrl_pkg_share, 'launch', 'kuka_controller.launch.py')
                ),
                launch_arguments = {'use_sim_time': use_sim_time}.items()
            )
        ]
    )
    
    arms = ['kuka_1', 'kuka_2', 'kuka_3', 'kuka_4']
    
    spawn_kuka_arm = [
        Node(
            package = 'ros_gz_sim',
            executable = 'create',
            arguments = [
                'topic', f'/{arm}/robot_description',
                'entity', 'kuka',
            ],
            output = 'screen',
        )
        for arm in arms  
    ]
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'true',
            description = 'use sim clock time'
        ),
        sim_node,
        kuka_arm_node,
        *spawn_kuka_arm
    ])
    