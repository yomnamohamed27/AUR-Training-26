import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    pkg_share = get_package_share_directory('workshop1')

    param_file = os.path.join(
        pkg_share,
        'config',
        'parameter.yaml'
    )

    turtle_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen'
    )

    go_to_goal_node = Node(
        package='workshop1',
        executable='go_to_goal',
        name='go_to_goal',
        output='screen',
        parameters=[param_file]
    )

    service_client_node = Node(
        package='workshop1',
        executable='service_cleintr',
        name='service_cleintr',
        output='screen'
    )

    return LaunchDescription([
        turtle_node,
        go_to_goal_node,
        service_client_node
    ])