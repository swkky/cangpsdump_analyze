# -+- coding: utf-8 -*-
#define log format
#1586782849.028696 can0 18F#00000E04FB659000
#1586782849.029193 can0 131#607900000000 1586782849.028479 3 34.730450 135.732034 1168231105 6.600000 116.584700 -0.127000 54
#1586782849.030431 can0 130#00000000FF8360
"""
row_
[0] = can_receive_time, [1] = can0, [2] = buf,
[3] = gps_fix_time, [4] = gps_mode(0-3),
[5] = latitude, [6] = longitude,   
[7] = altitude,
[8] = gps_speed, [9] = track,
[10] = climb, [11] = gps_fix_time_num
"""
row_can_receive_time = 1
row_buf = 2
row_gps_fix_time = 3
row_gps_mode = 4
row_latitude = 5
row_longitude = 6
row_altitude = 7
row_gps_speed = 8
row_track = 9
row_climb = 10
row_gps_fix_time_num = 11

row_num = 12