"""Motor class for individual motor control"""


class Motor:
    """Controls a single motor"""

    def __init__(self, port):
        """
        Initialize a motor.
        
        Args:
            port: Port of the motor (e.g., "A", "B", "C", "D", "E", "F")
        """
        self.port = port

    def start(self, speed=50):
        """
        Start the motor.
        
        Args:
            speed: Motor speed (-100 to 100)
        """
        pass

    def stop(self):
        """Stop the motor"""
        pass

    def run_for_degrees(self, degrees, speed=50):
        """
        Run motor for a specific number of degrees.
        
        Args:
            degrees: Degrees to rotate
            speed: Motor speed (-100 to 100)
        """
        pass

    def run_for_rotations(self, rotations, speed=50):
        """
        Run motor for a specific number of rotations.
        
        Args:
            rotations: Number of rotations
            speed: Motor speed (-100 to 100)
        """
        pass
