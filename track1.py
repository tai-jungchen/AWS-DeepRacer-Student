import math
import random

def reward_function(params):

    ##### off track reward #####
    is_offtrack = params['is_offtrack']
    offtrack_reward = 0.0
    
    if not is_offtrack:
        offtrack_reward = 3.0
    else:
        offtrack_reward = -1.0
    ##### off track reward #####
    
    ##### all wheel on track #####
    all_wheels_on_track = params['all_wheels_on_track']
    wheel_reward = 0.0
    
    if all_wheels_on_track:
        wheel_reward = 2.0
    else:
        wheel_reward = 1e-3
    ##### all wheel on track #####
    
    ##### Speed #####
    speed = params['speed']
    speed_reward = 0.0
    
    SPEED_THRESHOLD = 1.0
    if speed > SPEED_THRESHOLD:
        speed_reward = 1.0
    elif speed < 0.8:
        speed_reward = -1.0
    else:
        speed_reward = 1e-3
    ##### Speed #####
    
    ##### acceleration #####
    steering_angle = params['steering_angle']
    acc_reward = 0.0
    
    if abs(steering_angle) <= 5 and speed >= 1.0:
        acc_reward = 1.0
    elif abs(steering_angle) <= 20 and speed >= 0.8:
        acc_reward = 1.2
    else:
        acc_reward = 1e-4
    ##### acceleration #####
    
    ##### out-in-out reward #####
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    oio_reward = 0.0
    
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)
    
    theta_prime = abs(track_direction)
    
    if theta_prime > 90:
        theta_hat = 180 - theta_prime
    else:
        theta_hat = theta_prime
    
    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    marker_4 = 0.8 * track_width

    if theta_hat <= 30:    # straight line go to border
        if distance_from_center <= marker_1:
            oio_reward = 1e-3
        elif distance_from_center <= marker_2:
            oio_reward = 0.01
        elif distance_from_center <= marker_3:
            oio_reward = 0.1
        elif distance_from_center <= marker_4:
            oio_reward = 1.0
        else:    # likely crashed/ close to off track
            oio_reward = 1e-4
    else:    # corner go through center
        if distance_from_center <= marker_1:
            oio_reward = 1.0
        elif distance_from_center <= marker_2:
            oio_reward = 0.1
        elif distance_from_center <= marker_3:
            oio_reward = 0.01
        else:    # likely crashed/ close to off track
            oio_reward = 1e-4
    ##### out-in-out reward reward #####
    
    ##### steering #####
    heading = params['heading']
    
    steering_reward = 0.0

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 8.0
    if direction_diff > DIRECTION_THRESHOLD:
        steering_reward = 1e-4
    else:
        steering_reward = 1.0
    ##### steering #####
        
    reward = 10.0*oio_reward + 5.0*speed_reward + 5.0*wheel_reward + 10.0*steering_reward + 9.0*acc_reward + 10.0*offtrack_reward
    return float(reward)
