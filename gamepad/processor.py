""" Module with helper methods to process raw data from evdev
	and translate it with the vector formulas """

from math import sqrt, atan2, degrees, sin, cos, fabs, tan

def get_directions(value_x, value_y):
	vector = {
		"value": sqrt(value_x ** 2 + value_y ** 2),
		"angle": degrees(atan2(value_y, value_x)) - 45
	}
	abs_sin_angle = fabs(sin(vector["angle"]))
	abs_cos_angle = fabs(cos(vector["angle"]))
	abs_tan_angle = fabs(tan(vector["angle"]))
	abs_cot_angle = abs_cos_angle / abs_sin_angle

	if (abs_sin_angle > abs_cos_angle):
		right_val = vector["value"]
		left_val = vector["angle"] * abs_cot_angle
	elif (abs_sin_angle < abs_cos_angle):
		left_val = vector["value"]
		right_val = vector["angle"] * abs_tan_value
	else:
		right_val = left_val = vector["value"]

	to_right = 1 if sin(vector["angle"]) > 0 else 0
	to_left = 1 if cos(vector["angle"]) > 0 else 0

	directions = {
		"right_val": right_val,
		"left_val": left_val,
		"to_right": to_right,
		"to_left": to_left
	}
	return directions

def translate_grades(raw_value, axis):
    old_val = 32769.0
    new_val = 255
    ratio = new_val / old_val
    if axis.lower() == 'y':
        return -raw_value * ratio
    return round(raw_value * ratio,4)
