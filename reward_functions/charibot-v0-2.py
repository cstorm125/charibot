# from https://medium.com/axel-springer-tech/how-to-win-aws-deepracer-ce15454f594a
# discount 0.9; 360 mins
# steering: -20, 0, 20
# speed: 1, 2, 3

import math


def get_direction_diff(params):
    next_point = params["waypoints"][params["closest_waypoints"][1]]
    prev_point = params["waypoints"][params["closest_waypoints"][0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(
        next_point[1] - prev_point[1], next_point[0] - prev_point[0]
    )
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - params["heading"])
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    return direction_diff


def speeding(params, power=2, speed_range=[0, 5]):
    # polynomial smoothing of speed [0,1]
    max_speed_reward = speed_range[1] ** power
    min_speed_reward = speed_range[0] ** power
    abs_speed_reward = params["speed"] ** 2
    speed_reward = (abs_speed_reward - min_speed_reward) / (
        max_speed_reward - min_speed_reward
    )
    return speed_reward


def heading(params):
    # linear decrease the higher direction differences are [0,1]
    abs_heading_reward = 1 - (get_direction_diff(params) / 180.0)
    return abs_heading_reward


def steering(params):
    # triangluar [0,1]
    direction_diff = get_direction_diff(params)
    return 1 - (abs(params["steering_angle"] - direction_diff) / 180.0)


def reward_function(params):
    speed_reward = speeding(params)
    heading_reward = heading(params)
    steering_reward = steering(params)
    total_reward = (
        40 * speed_reward + 40 * heading_reward + 20 * steering_reward
    )

    if params["progress"] > 90:
        total_reward += progress

    # #need for speed
    # if params["speed"] < 1:
    # 	total_reward*=0.9

    # don't fall off track
    if not params["all_wheels_on_track"]:
        return 1e-3
    else:
        return total_reward
