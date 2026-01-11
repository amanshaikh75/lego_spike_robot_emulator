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


def move(
    pair: int,
    steering: int,
    *,
    velocity: int = 360,
    acceleration: int = 1000,
) -> None:
    """
    Move the motor pair.
    
    Args:
        steering: Steering value (-100 to 100, 0 = straight,
            positive = right, negative = left)
        velocity: Velocity in degrees per second (default 360)
        acceleration: Acceleration in degrees per second squared
            (default 1000)
    """
    # validate inputs
    if not isinstance(pair, int):
        raise TypeError("pair must be an int")
    if not isinstance(steering, int):
        raise TypeError("steering must be an int")
    if not -100 <= steering <= 100:
        raise ValueError("steering must be between -100 and 100")
    if not isinstance(velocity, int):
        raise TypeError("velocity must be an int")
    if not isinstance(acceleration, int):
        raise TypeError("acceleration must be an int")

    # ensure pairs registry exists and the requested pair is defined
    try:
        pairs = _PAIRS
    except NameError:
        raise KeyError("no motor pairs defined")
    if pair not in pairs:
        raise KeyError(f"pair {pair!r} is not defined")

    # simple differential steering mix:
    # - steering == 0 -> both wheels same velocity
    # - steering > 0  -> turn right: left wheel runs at full velocity,
    #                    right wheel is scaled down
    # - steering < 0  -> turn left: right wheel runs at full velocity,
    #                    left wheel is scaled down
    if steering == 0:
        left_vel = right_vel = velocity
    elif steering > 0:
        left_vel = velocity
        right_vel = int(velocity * (100 - steering) / 100)
    else:  # steering < 0
        right_vel = velocity
        left_vel = int(velocity * (100 + steering) / 100)

    # store the commanded wheel velocities in a simple in-memory registry
    try:
        _COMMANDS
    except NameError:
        _COMMANDS: dict[int, dict[str, int]] = {}
        globals()["_COMMANDS"] = _COMMANDS

    _COMMANDS[pair] = {
        "left_velocity": left_vel,
        "right_velocity": right_vel,
        "acceleration": acceleration,
    }


def stop(pair: int) -> None:
    """Stop the motor pair."""
    if not isinstance(pair, int):
        raise TypeError("pair must be an int")

    try:
        pairs = _PAIRS
    except NameError:
        raise KeyError("no motor pairs defined")
    if pair not in pairs:
        raise KeyError(f"pair {pair!r} is not defined")

    try:
        _COMMANDS
    except NameError:
        _COMMANDS: dict[int, dict[str, int]] = {}
        globals()["_COMMANDS"] = _COMMANDS

    _COMMANDS[pair] = {"left_velocity": 0, "right_velocity": 0, "acceleration": 0}
