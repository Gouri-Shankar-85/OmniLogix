#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction,
    SetEnvironmentVariable
)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    
    ctrl_pkg = 'omnilogix_controller'
    ctrl_pkg_share = get_package_share_directory(ctrl_pkg)
    
    sim_pkg = 'omnilogix_simulation'
    sim_pkg_share = get_package_share_directory(sim_pkg)
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    desc_pkg = 'kuka_description'
    desc_pkg_share = get_package_share_directory(desc_pkg)
    
    # set GZ_SIM_RESOURCE_PATH to find the xacro files in kuka_description package
    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.path.dirname(desc_pkg_share)
    )
    
    # launch gazebo sim with empty world
    sim_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(sim_pkg_share, 'launch', 'empty_gz.launch.py')
        ),
        launch_arguments = {'use_sim_time': use_sim_time}.items()
    )
    
    # list of arms with their spawn poses
    arms = [
        ('kuka_1',  0.0,  0.0, 0.0),
        ('kuka_2',  5.0,  0.0, 0.0),
        ('kuka_3',  0.0,  5.0, 0.0),
        ('kuka_4',  5.0,  5.0, 0.0),
    ]
    
    # spawn arms in gz in 4 different poses
    spawn_arms = TimerAction(
        period=5.0,                             
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-topic', f'/{arm}/robot_description',   
                    '-name',  arm,        
                    '-x', str(x),
                    '-y', str(y),
                    '-z', str(z),                   
                ],
                output='screen',
            )
            for arm, x, y, z in arms
        ]
    )

    # launch arm controller node with delay time
    kuka_arm_node = TimerAction(
        period=10.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(ctrl_pkg_share, 'launch', 'kuka_controller.launch.py')
                ),
                launch_arguments={'use_sim_time': use_sim_time}.items()
            )
        ]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'true',
            description = 'use sim clock time'
        ),
        set_gz_resource_path,
        sim_node,
        spawn_arms,
        kuka_arm_node
    ])
    