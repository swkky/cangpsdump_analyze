# -+- coding: utf-8 -*-
import sys
import numpy as np
import gpxpy
import folium
import matplotlib.pyplot as p
#low example
#1586323807.137337 can0 180#0314BF1C0D1BED00 1586323806.312156 3 34.706861 135.706305 0 14.569000 169.199300 -0.194000 4
#"%010ld.%06ld %*s %s %f %d %f %f %d %f %f %f %d\n",
"""
[0] = can_receive_time, [1] = can0, [2] = buf,
[3] = gps_fix_time, [4] = gps_mode(0-3),
[5] = latitude, [6] = longitude,   
[7] = altitude,
[8] = gps_speed, [9] = track,
[10] = climb, [11] = gps_fix_time_num
"""

#時間のずれをチェックする
def check_time_gap(file_path):
    #if start gps fix fix_flag turns 1
    fix_flag = 0
    previous_gps_count = -1
    when_gps_fix = []
    one_before_gps_fix = []
    buffer = []
    time_gap_first_can_message_when_gps_fix = []
    time_gap_last_can_message_when_gps_fix = []
    #gps_points[[latitude],[longitude]]
    #process for log file
    logfile = open(file_path, 'r')
    for line in logfile:
        line_spt = line.split()
        #end of file
        if len(line_spt) < 12:
            break
        can_receive_time = float(line_spt[0])
        gps_fix_time = float(line_spt[3])
        fix_status = int(line_spt[4])
        latitude = float(line_spt[5])
        longitude = float(line_spt[6])
        gps_speed = float(line_spt[8])
        gps_track = float(line_spt[9])
        gps_count = int(line_spt[11])
        #GPS fix start
        if fix_flag == 0 and fix_status != 0:
            previous_gps_count = 1
            fix_flag = 1
            """
        if fix_flag == 1:
            print(can_receive_time,gps_fix_time)
            """
        #GPS fix change after second times(first CAN message when gps data change)
        if previous_gps_count != gps_count and fix_status != 0:
            previous_gps_count = gps_count
            when_gps_fix.append([can_receive_time,gps_fix_time,gps_count])
            print(gps_count,can_receive_time,gps_fix_time)
            time_gap = can_receive_time - gps_fix_time
            time_gap_first_can_message_when_gps_fix.append(time_gap)
            print('Time gap %f\n'  %time_gap)
            #print(can_receive_time)
            #print(gps_count,latitude,longitude,gps_speed,gps_track)
"""
    for i in range(len(when_gps_fix)):
        print(when_gps_fix[i])
"""