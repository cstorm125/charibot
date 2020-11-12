def reward_function(params):
    track_width = params["track_width"]
    distance_from_center = params["distance_from_center"]
    all_wheels_on_track = params["all_wheels_on_track"]
    speed = params["speed"]
    steering = abs(
        params["steering_angle"]
    )  # Only need the absolute steering angle
    SPEED_THRESHOLD = 1.0
    ABS_STEERING_THRESHOLD = 15

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # 1 stay close to center line
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # 2 don't fall off track
    if not all_wheels_on_track:
        # Penalize if the car goes off track
        reward = 1e-3
    # 3 go fast
    elif speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward += 0.5
    else:
        # High reward if the car stays on track and goes fast
        reward += 1.0

    # 4 don't go zigzag too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)
