from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():
    sitl = ExecuteProcess(
        cmd=[
            "sim_vehicle.py",
            "-v", "ArduCopter",
            "--out=udp:127.0.0.1:14540"
        ],
        cwd="/home/dattu/ardupilot/Tools/autotest",
        output="screen"
    )
    
    geofence = Node(
        package="survey_system",
        executable="geofence_node",
        name="geofence_node",
        output="screen"
    )
    
    return LaunchDescription([
        sitl,
        geofence
    ])
