""" Module with helper methods to process raw data from evdev
	and translate it with the vector formulas """

from math import sqrt, atan2, degrees, sin, cos, fabs, tan, radians

def get_directions3(value_x, value_y):
    vector = {
        "value": sqrt(value_x ** 2 + value_y ** 2),
        "angle": degrees(atan2(value_y, value_x)) - 45
    }
    abs_sin_angle = fabs(sin(radians(vector["angle"])))
    abs_cos_angle = fabs(cos(radians(vector["angle"])))
    abs_tan_angle = fabs(tan(radians(vector["angle"])))

    if abs_sin_angle != 0:
        abs_cot_angle = abs_cos_angle / abs_sin_angle

    if (abs_sin_angle > abs_cos_angle):
        right_val = vector["value"]
        left_val = vector["value"] * abs_cot_angle
    elif (abs_sin_angle < abs_cos_angle):
        left_val = vector["value"]
        right_val = vector["value"] * abs_tan_angle
    else:
        right_val = left_val = vector["value"]

    to_right = 1 if sin(radians(vector["angle"])) > 0 else 0
    to_left = 1 if cos(radians(vector["angle"])) > 0 else 0


    directions = {
		"right_val": round(right_val),
		"left_val": round(left_val),
		"to_right": to_right,
		"to_left": to_left
	}
    return directions

def get_directions2(value_x, value_y, trigger_value):
    angle = degrees(atan2(value_y, value_x)) % 360
    vmax = trigger_value
    cos_angle = cos(radians(angle))

    if 0 <= angle and angle <= 90:
        wl_value = vmax
        wr_value = wl_value - vmax * cos_angle
        dl_value = dr_value = 1
    elif 90 < angle and angle <= 180:
        wr_value = vmax
        wl_value = wr_value + vmax * cos_angle
        dl_value = dr_value = 1
    elif 180 < angle and angle <= 270:
        wr_value = vmax
        wl_value = wr_value + vmax * cos_angle
        dl_value = dr_value = -1
    elif angle < 360:
        wl_value = vmax
        wr_value = wl_value - vmax  * cos_angle
        dl_value = dr_value = -1

    directions = {
        "right_val": round(wr_value),
        "left_val": round(wl_value),
        "to_right": dl_value,
        "to_left": dr_value
    }
    return directions


def get_directions(value_x, left_trigger, right_trigger):

    left_dir, right_dir, right_motor, left_motor = 0,0,0,0

    if left_trigger > 0:
        left_dir = 0
        right_dir = 0
        right_motor = left_trigger
        left_motor = left_trigger
        if value_x > 5:
            right_motor = left_trigger - value_x
            left_motor = left_trigger
        elif value_x < -5:
            right_motor = left_trigger
            left_motor = left_trigger + value_x
    elif right_trigger > 0:
        left_dir = 1
        right_dir = 1
        right_motor = right_trigger
        left_motor = right_trigger
        if value_x > 5:
            right_motor = right_trigger - value_x
            left_motor = right_trigger
        elif value_x < -5:
            right_motor = right_trigger
            left_motor = right_trigger + value_x
    else:
        if value_x > 5:
            right_motor = value_x
            left_motor = value_x
            left_dir = 0
            right_dir = 1
        elif value_x < -5:
            right_motor = -value_x
            left_motor = -value_x
            left_dir = 1
            right_dir = 0

    right_motor = 0 if right_motor < 0 else right_motor
    left_motor = 0 if left_motor < 0 else left_motor

    directions = {
        "right_val": int(right_motor),
        "left_val": int(left_motor),
        "to_right": right_dir,
        "to_left": left_dir
    }
    return directions

def get_directions_alt(value_x , left_trigger, right_trigger):

    print value_x, left_trigger, right_trigger

    if left_trigger == 0 and right_trigger == 0:
        right_motor = -value_x
        left_motor = value_x
    elif left_trigger == 0:
        right_motor = right_trigger - value_x
        left_motor = right_trigger + value_x
    elif right_trigger == 0:
        right_motor = - left_trigger + value_x
        left_motor = - left_trigger - value_x
    else:
        right_motor = 0
        left_motor = 0

    right_dir = 1 if right_motor >= 0 else 0
    left_dir = 1 if left_motor >= 0 else 0

    right_motor = 255 if abs(right_motor) > 255 else abs(right_motor)
    left_motor = 255 if abs(left_motor) > 255 else abs(left_motor)

    right_motor = 0 if right_motor <= 5 else right_motor
    left_motor = 0 if left_motor <= 5 else left_motor

    right_motor = 0 if right_motor < 0 else right_motor
    left_motor = 0 if left_motor < 0 else right_motor
    directions = {
        "right_val": int(right_motor),
        "left_val": int(left_motor),
        "to_right": right_dir,
        "to_left": left_dir
    }

    return directions


def translate_grades(raw_value, axis):
    old_val = 32769.0
    new_val = 255
    ratio = new_val / old_val
    if axis.lower() == 'y':
        return -raw_value * ratio
    return round(raw_value * ratio,4)
