#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, 
    IncludeLaunchDescription,
    TimerAction
)
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node

def generate_launch_description():
    
    desc_pkg_name = 'kuka_description'
    desc_pkg_share = get_package_share_directory(desc_pkg_name)
    
    ctrl_pkg_name = 'omnilogix_controller'
    ctrl_pkg_share = get_package_share_directory(ctrl_pkg_name)

    use_sim_time = LaunchConfiguration('use_sim_time')
    
    arms = ['kuka_1', 'kuka_2', 'kuka_3', 'kuka_4']
    
    desc_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(desc_pkg_share, 'launch', 'kuka_rviz.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )
    
    controller_managers = [
        Node(
            package = 'controller_manager',
            executable = 'ros2_control_node',
            parameters = [
                os.path.join(ctrl_pkg_share, 'config', f'{arm}_controller.yaml'),
                {'use_sim_time': use_sim_time}
            ],
            output = 'screen',
        )
        for arm in arms
    ]
    
    # Spawn controllers with delay_time so that rsp_node is up
    spawner_nodes = TimerAction(
        period = 5.0,
        actions = [
            Node(
                package = 'controller_manager',
                executable = 'spawner',
                namespace = arm,
                arguments = [
                    'joint_state_broadcaster',
                    '--controller-manager', f'/{arm}/controller_manager'
                ],
                output = 'screen',
            )
            for arm in arms
        ] + [
            Node(
                package = 'controller_manager',
                executable = 'spawner',
                namespace = arm,
                arguments = [
                    f'{arm}_controller',
                    '--controller-manager', f'/{arm}/controller_manager'
                ],
                output = 'screen',
            )
            for arm in arms
        ]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'false',
            description = 'If true: use simulation clock time'
        ),
        desc_launch,
        *controller_managers,
        spawner_nodes
    ])
    
    