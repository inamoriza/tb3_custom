# Standard library imports
import os

# Related third party imports
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description() -> LaunchDescription:

    # Initialize the launch description
    ld = LaunchDescription()

    # Get the launch file directory path for the "tb3_custom" package
    launch_file_dir = os.path.join(
        get_package_share_directory("tb3_custom"), "launch"
    )
    
    # Get the path to Gazebo folder and the world model
    ros_gz_sim = get_package_share_directory("ros_gz_sim")
    world = os.path.join(
        get_package_share_directory("tb3_custom"),
        "worlds",
        "obstacle_course.sdf"
    )

    # Set up configuration parameters
    use_sim_time = LaunchConfiguration("use_sim_time", default = "false")
    x_pose = LaunchConfiguration("x_pose", default = "0.0")
    y_pose = LaunchConfiguration("y_pose", default = "0.0")

    # Gazebo server launch description
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments = {
            "gz_args": f"-r -s -v2 {world}", "on_exit_shutdown": "true"
        }.items()
    )

    # Gazebo client launch description
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments = {
            "gz_args": "-g -v2", "on_exit_shutdown": "true"
        }.items()
    )

    # Combine all launch descriptions
    ld.add_action(gzserver)
    ld.add_action(gzclient)

    return ld