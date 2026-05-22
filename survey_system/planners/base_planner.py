from abc import ABC, abstractmethod
from geometry_msgs.msg import Polygon


class BasePlanner(ABC):
    @abstractmethod
    def generate_waypoints(self, geofence: Polygon) -> Polygon:
        pass
