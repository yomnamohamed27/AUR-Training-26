import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class service_client(Node):
    def __init__(self):
        super().__init__("service_client")
        self.client = self.create_client(SetBool, "start_motion")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available")
        self.timer = self.create_timer(3.0, self.send_request)
        self.request = False

    def send_request(self):
        self.request = True
        request = SetBool.Request()
        request.data = True
        future = self.client.call_async(request)
        future.add_done_callback(self.response_callback) 
        self.timer.cancel()

    def response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info("Motion started successfully")
            else:
                self.get_logger().info("Failed to start motion")
        except Exception as e:
            self.get_logger().error(f"Service failed: {e}")



def main(args=None):
    rclpy.init(args=args)
    node = service_client()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()