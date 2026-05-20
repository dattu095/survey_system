import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Polygon


class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner_node')
        
        self.geofence_subscriber = self.create_subscription(
            Polygon,
            '/drone/geofence',
            self.geofence_callback,
            10
        )
        
        self.waypoint_publisher = self.create_publisher(
            Polygon,
            '/drone/waypoints',
            10
        )

        self.geofence = None

    def _polygon_equal(self, poly1: Polygon, poly2: Polygon, tol=1e-6):
        if len(poly1.points) != len(poly2.points):
            return False
        
        for p1, p2 in zip(poly1.points, poly2.points):
            if abs(p1.x - p2.x) > tol:
                return False
            
            if abs(p1.y - p2.y) > tol:
                return False
            
            if abs(p1.z - p2.z) > tol:
                return False
        
        return True

    def get_waypoints(self):
        return self.geofence

    def geofence_callback(self, msg):
        if self.geofence is None:
            self.get_logger().debug("Initial geofence received")

            self.geofence = msg
            self.waypoint_publisher.publish(self.get_waypoints())
            
            return
        
        if not self._polygon_equal(msg, self.geofence):
            self.get_logger().debug("Geofence changed")

            self.geofence = msg
            self.waypoint_publisher.publish(self.get_waypoints())
            
            return
        
        self.get_logger().debug("No geofence change") 
            
    
def main(args=None):
    rclpy.init(args=args)

    node = PathPlannerNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().error("abort")

    finally:
        node.destroy_node()

        rclpy.shutdown()

if __name__ == "__main__":
    main()
