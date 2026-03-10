import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 获取功能包的share路径
    urdf_package_path = get_package_share_directory('fishbot_description')
 
    default_xacro_path = os.path.join(urdf_package_path, 'urdf', 'fishbot', 'fishbot.urdf.xacro')
    #default_rviz_config_path = os.path.join(urdf_package_path, 'config', 'display_robot_model.rviz')
    default_gazebo_world_path = os.path.join(urdf_package_path, 'world', 'custom_room_world')
    # 声明一个urdf目录的参数，方便修改

    action_declare_arg_model_path = launch.actions.DeclareLaunchArgument(
        name='model',
        default_value=str(default_xacro_path),
        description='URDF的绝对路径'
    )
    
    substitutions_command_result = launch.substitutions.Command(
        ['xacro ', launch.substitutions.LaunchConfiguration('model')]
    )

    # 创建机器人描述参数值
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(
        substitutions_command_result,
        value_type=str
    )

    # 启动robot_state_publisher节点
    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',  # 修复exec_name为executable
        parameters=[{'robot_description': robot_description_value}]  # 修复拼写和语法错误
    )

    # 启动joint_state_publisher节点
    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher'  # 修复exec_name为executable
    )

    # 启动rviz2节点
    # action_rviz_node = launch_ros.actions.Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     arguments=['-d',default_rviz_config_path ]  

    # )
    # 启动gazebo节点
    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('gazebo_ros'), '/launch/gazebo.launch.py']
        ),
        launch_arguments=[('world', default_gazebo_world_path), ('verbose', 'true')]
    )

    # 启动spawn_entity节点，将机器人放入Gazebo
    action_spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'fishbot'],
        output='screen'
    )

    # 返回启动描述
    return launch.LaunchDescription([
        action_declare_arg_model_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        # action_rviz_node
        action_launch_gazebo,
        action_spawn_entity
    ])
