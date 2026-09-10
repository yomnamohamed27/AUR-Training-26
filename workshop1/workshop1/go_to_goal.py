import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import SetBool

'''TARGET_X = 10.0  # Target X coordinate for the turtle to reach
TARGET_Y = 10.0  # Target Y coordinate for the turtle to reach
KP_LINEAR = 1.5  # Proportional gain for linear velocity
KP_ANGULAR = 6.0  # Proportional gain for angular velocity
DISTANCE_TOLERANCE = 0.1  # Distance error limit to consider goal reached
ANGLE_TOLERANCE = 0.05  # Heading alignment threshold before moving forward
LOOP_RATE = 20  # Control loop frequency in Hz'''



class GoToGoal(Node):
    def __init__(self):
        super().__init__('go_to_goal')
        self.declare_parameter('robot_name', 'turtle1')
        self.declare_parameter('target_x' , 10.0)
        self.declare_parameter('target_y' , 10.0)
        self.declare_parameter('linear_gain' , 1.5)
        self.declare_parameter('angular_gain' , 6.0)
        self.declare_parameter('distance_tolerance' , 0.1)
        self.declare_parameter('angle_tolerance' , 0.05)
        self.declare_parameter('loop_rate' , 20)

        
        self.target_x=self.get_parameter('target_x').value
        self.target_y=self.get_parameter('target_y').value
        self.linear_gain=self.get_parameter('linear_gain').value
        self.angular_gain=self.get_parameter('angular_gain').value
        self.distance_tolerance=self.get_parameter('distance_tolerance').value
        self.angle_tolerance=self.get_parameter('angle_tolerance').value
        self.loop_rate=self.get_parameter('loop_rate').value    

        # Target Goal Coordinates
        self.goal_x = self.target_x
        self.goal_y = self.target_y

        # Proportional Gains (K_p)
        self.kp_linear = self.linear_gain
        self.kp_angular = self.angular_gain

        # Tolerances
        self.distance_tolerance = self.distance_tolerance  # Distance error limit to consider goal reached
        self.angle_tolerance = self.angle_tolerance    # Heading alignment threshold before moving forward

        # State Variables
        self.active_motion= False
        self.goal_reached = False
        self.current_pose = None

        # ROS 2 Publisher & Subscriber
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_subscriber = self.create_subscription( Pose, '/turtle1/pose', self.pose_callback, 10)

        self.service = self.create_service(SetBool, 'start_motion', self.start_motion_callback)


        '''if self.active_motion is False:
            self.get_logger().info("Waiting for initial pose data...")
            return'''
        
        # Control Loop running at 20 Hz
        self.timer = self.create_timer(1.0 / self.loop_rate, self.control_loop)

        self.get_logger().info(f'Navigating turtle to target goal: ({self.goal_x}, {self.goal_y})')

        def pose_callback(self, msg: Pose):
            """Update current position and heading from /turtle1/pose stream."""
            self.current_pose = msg

        def start_motion_callback(self, request, response):
            if request.data is True:
                self.get_logger().info("Motion activated")
                self.active_motion = True
                self.goal_reached = False
                response.success = True
                response.message = "Motion started"
            else:
                self.get_logger().info("Motion deactivated")
                response.success = False
                response.message = "Motion stopped."
            return response 


        def normalize_angle(self, angle: float) -> float:
            while angle > math.pi:
                angle -= 2.0 * math.pi
            while angle < -math.pi:
                angle += 2.0 * math.pi
            return angle

    def control_loop(self):
        """Proportional Control Loop."""
        if self.active_motion == False or self.goal_reached:
            return

        if self.current_pose is None:
            self.get_logger().info("Waiting")
            return
        # 1. Calculate Cartesian Errors
        dx = self.goal_x - self.current_pose.x
        dy = self.goal_y - self.current_pose.y

        # Euclidean Distance Error: sqrt((x_g - x)^2 + (y_g - y)^2)
        distance_error = math.sqrt(dx**2 + dy**2)

        # Desired Heading Angle: atan2(dy, dx)
        target_angle = math.atan2(dy, dx)
        heading_error = self.normalize_angle(target_angle - self.current_pose.theta)

        msg = Twist()

        # 2. Check if Goal is Reached
        if distance_error < self.distance_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_vel_publisher.publish(msg)
            self.goal_reached = True
            self.active_motion = False
            self.get_logger().info('Goal Reached Successfully!')
            return

        # 3. Proportional Control Logic
        # If heading error is large, align facing direction first before moving forward
        if abs(heading_error) > self.angle_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = self.kp_angular * heading_error
        else:
            # Scale forward speed and heading alignment concurrently
            msg.linear.x = min(self.kp_linear * distance_error, 2.0)  # Cap speed at 2.0 m/s
            msg.angular.z = self.kp_angular * heading_error

        self.cmd_vel_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = GoToGoal()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
