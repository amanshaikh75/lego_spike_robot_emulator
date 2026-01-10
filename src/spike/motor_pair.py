"""MotorPair class for paired motor control"""


class MotorPair:
    """Controls a pair of motors for movement"""

    def __init__(self, left_port, right_port):
        """
        Initialize motor pair.
        
        Args:
            left_port: Port of the left motor
            right_port: Port of the right motor
        """
        self.left_port = left_port
        self.right_port = right_port

    def move(self, distance, unit="cm", steering=0, speed=50):
        """
        Move the robot forward or backward.
        
        Args:
            distance: Distance to move
            unit: Unit of distance ("cm", "in", "rotations")
            steering: Steering angle (-100 to 100, 0 = straight)
            speed: Motor speed (0-100)
        """
        pass

    def turn(self, angle, radius=None, speed=50):
        """
        Turn the robot.
        
        Args:
            angle: Angle to turn in degrees (positive = right, negative = left)
            radius: Turn radius (None = pivot turn)
            speed: Motor speed (0-100)
        """
        pass

    def move_tank(self, left_speed, right_speed, duration=None, distance=None):
        """
        Control left and right motors independently (tank-style).
        
        Args:
            left_speed: Left motor speed (-100 to 100)
            right_speed: Right motor speed (-100 to 100)
            duration: Duration in seconds
            distance: Distance to move
        """
        pass

    def stop(self):
        """Stop the motors"""
        pass
