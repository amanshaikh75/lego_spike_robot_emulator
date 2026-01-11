"""Motor pair module for paired motor control"""
def pair(pair: int, left_motor: int, right_motor: int) -> None:
    """
    Define a motor pair.
    
    Args:
        pair: Identifier for the motor pair
        left_motor: Port number for the left motor
        right_motor: Port number for the right motor
    """
    # simple in-memory registry of defined pairs
    try:
        _PAIRS
    except NameError:
        _PAIRS: dict[int, tuple[int, int]] = {}
        globals()["_PAIRS"] = _PAIRS

    if not isinstance(pair, int):
        raise TypeError("pair must be an int")
    if not isinstance(left_motor, int) or not isinstance(right_motor, int):
        raise TypeError("left_motor and right_motor must be ints")
    if left_motor == right_motor:
        raise ValueError("left_motor and right_motor must be different ports")

    _PAIRS[pair] = (left_motor, right_motor)


def move(pair: int, steering: int, *, velocity: int = 360, acceleration: int = 1000) -> None:
    """
    Move the motor pair.
    
    Args:
        steering: Steering value (-100 to 100, 0 = straight, positive = right, negative = left)
        velocity: Velocity in degrees per second (default 360)
        acceleration: Acceleration in degrees per second squared (default 1000)
    """
    pass


def stop(pair: int) -> None:
    """Stop the motor pair."""
    pass
