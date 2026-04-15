import math
import time

def get_magnitude(data):
    """Calculates total force (Resultant Vector)"""
    return [math.sqrt(sum((val-90)**2 for val in data))]

def get_tilt_angles(accel):
    """
    Converts gravity distribution into Tilt (Degrees).
    Works best when the device is moving slowly.
    """
    x, y, z = accel
    # math.atan2 is safer than atan as it handles division by zero
    pitch = math.atan2(x, math.sqrt(y*y + z*z)) * 180 / math.pi
    roll = math.atan2(y, math.sqrt(x*x + z*z)) * 180 / math.pi
    yaw = math.atan2(z, math.sqrt(x*x + y*y)) * 180 / math.pi
    return [pitch, roll, yaw]

current_angle = [0,0,0]
def get_gyro_angles(gyro):
    """
    Integrates angular velocity to find position.
    Requires knowing how much time has passed (dt).
    """
    global current_angle
    x, y, z = gyro
    
    dt = 0.01

    angle_x = current_angle[0] + (x * dt)
    angle_y = current_angle[1] + (y * dt)
    angle_z = current_angle[2] + (z * dt)

    # New Angle = Old Angle + (Speed * Time)
    current_angle = [angle_x,angle_y,angle_z]

    return [angle_x,angle_y,angle_z]

def low_pass_filter(new_val, prev_filtered, alpha=0.1):
    """
    Smooths out jitter. 
    alpha 0.1 = 90% old data, 10% new data.
    """
    return (alpha * new_val) + (1.0 - alpha) * prev_filtered
