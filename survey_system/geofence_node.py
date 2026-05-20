import threading
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Polygon, Point32

from mavsdk import System

import asyncio


class GeofenceNode(Node):
    def __init__(self):
        super().__init__("geofence_node")

        # Publishers
        self.home_pub = self.create_publisher(NavSatFix, "/drone/home", 10)

        self.geofence_pub = self.create_publisher(Polygon, "/drone/geofence", 10)

        self.home = NavSatFix()
        self.geofence = Polygon()

        self.drone = System()
        asyncio.run(self.connect())

        self.loop = asyncio.new_event_loop()

        self.thread = threading.Thread(target=self.start_loop, daemon=True)

        self.thread.start()

        # ROS timer
        self.timer = self.create_timer(1.0, self.publish_topics)

    def start_loop(self):
        asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(self.main_async())

    async def main_async(self):
        await self.connect()

        await asyncio.gather(self.update_home(), self.update_geofence())

    def publish_topics(self):
        self.home_pub.publish(self.home)
        self.geofence_pub.publish(self.geofence)

    async def connect(self):
        await self.drone.connect(system_address="udpin://0.0.0.0:14540")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                self.get_logger().info("Connected to ArduPilot")
                break

    async def update_home(self):
        while True:
            try:
                async for h in self.drone.telemetry.home():
                    self.home = NavSatFix(
                        latitude=h.latitude_deg,
                        longitude=h.longitude_deg,
                        altitude=h.absolute_altitude_m,
                    )
                    break

            except Exception:
                continue

    async def update_geofence(self):
        while True:
            try:
                tmp_geofence = await self.drone.mission_raw.download_geofence()

                self.geofence.points = list(
                    map(
                        lambda point: Point32(
                            x=point.x / 1e7, y=point.y / 1e7, z=point.z / 1e7
                        ),
                        tmp_geofence,
                    )
                )

            except Exception:
                continue


def main(args=None):
    rclpy.init(args=args)

    node = GeofenceNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().error("abort")

    finally:
        node.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":
    main()
