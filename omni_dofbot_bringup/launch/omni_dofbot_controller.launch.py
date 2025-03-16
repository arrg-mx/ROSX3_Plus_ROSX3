from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.substitutions import Command
import os
from ament_index_python.packages import get_package_share_path

from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.event_handlers import OnProcessExit

def generate_launch_description():

    # Ruta del archivo URDF
    urdf_path = os.path.join(get_package_share_path('omni_dofbot_description'),
                             'urdf', 'omni_dofbot_trajectory_controller.xacro')
    # Ruta del archivo RVIZ
    rviz_config_path = os.path.join(get_package_share_path('omni_dofbot_bringup'),
                                    'rviz', 'omni_dofbot_trayectory_rviz.rviz')
    
    # Definición del parámetro de la ruta del archivo URDF
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    world = os.path.join(
        get_package_share_path('dofbot_bringup'),
        'world',
        'test_world.world'
    )

    # Gazebo
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
                    launch_arguments={'world': world}.items()
             )
    
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'omni_dofbot'],
                        output='screen')

    # Ejecución del nodo robot_state_publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}]
    )

    # Ejecución del nodo de RVIZ
    config_arg = DeclareLaunchArgument(name='rvizconfig', default_value=rviz_config_path)
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )

    dofbot_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'dofbot_trajectory_controller'],
        output='screen'
    )

    dofbot_gripper_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'dofbot_gripper_controller'],
        output='screen'
    )

    wheel_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'wheel_velocity_controller'],
        output='screen'
    )

    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen' 
    )
    
    # Retorno de la función del archivo launch
    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_state_controller],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[dofbot_controller],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[dofbot_gripper_controller],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[wheel_controller],
            )
        ),
        robot_state_publisher_node,
        config_arg,
        rviz2_node,
        gazebo,
        spawn_entity
    ])
