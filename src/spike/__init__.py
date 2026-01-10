"""LEGO Spike Prime API mock/wrapper for emulation"""

from .motor_pair import MotorPair
from .motor import Motor
from .hub import Hub

__all__ = ["MotorPair", "Motor", "Hub"]
