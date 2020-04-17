# -+- coding: utf-8 -*-
import sys
import numpy as np
import gpxpy
import folium
import matplotlib.pyplot as plt
import my_module.log_format as lf
#low example
#1586323807.137337 can0 180#0314BF1C0D1BED00 1586323806.312156 3 34.706861 135.706305 0 14.569000 169.199300 -0.194000 4
"""
lf.row_
[0] = can_receive_time, [1] = can0, [2] = buf,
[3] = gps_fix_time, [4] = gps_mode(0-3),
[5] = latitude, [6] = longitude,   
[7] = altitude,
[8] = gps_speed, [9] = track,
[10] = climb, [11] = gps_fix_time_num
"""

#ログデータから緯度，経度(同一データ無し)のみを取り出して経路をhtmlで出力
def show_route_from_gps(file_path):
	#if start gps fix fix_flag turns 1
	fix_flag = 0
	previous_gps_count = -1
	#gps_points[[latitude],[longitude]]
	gps_points = []
	#process for log file
	logfile = open(file_path, 'r')
	for line in logfile:
		line_spt = line.split()
		#print(len(line_spt))
		#end of file
		if len(line_spt) < 3:
			break
		if len(line_spt) == lf.row_num:
			fix_status = int(line_spt[lf.row_gps_mode])
			latitude = float(line_spt[lf.row_latitude])
			longitude = float(line_spt[lf.row_longitude])
			gps_speed = float(line_spt[lf.row_gps_speed])
			gps_track = float(line_spt[lf.row_track])
			gps_count = int(line_spt[lf.row_gps_fix_time_num])
			#GPS fix start 
			if fix_flag == 0 and fix_status != 0:
				previous_gps_count = 1
				fix_flag = 1
			#GPS fix after second times
			if previous_gps_count != gps_count and fix_status > 1:
				previous_gps_count = gps_count
				#print(gps_count,latitude,longitude,gps_speed,gps_track)
				gps_points.append([latitude,longitude])
	#################################################
	# create map
	#################################################
	#print(gps_points)
	map = folium.Map(location=[gps_points[0][0],gps_points[0][1]], zoom_start=20)
	# add map tiling options
	folium.TileLayer('Mapbox Bright').add_to(map)
	folium.TileLayer('cartodbdark_matter').add_to(map)
	folium.TileLayer('openstreetmap').add_to(map)
	folium.LayerControl().add_to(map)
	folium.PolyLine(locations = gps_points).add_to(map)
	#create Icon of start(blue) and end(red)
	folium.Marker(
		location= (gps_points[0][0],gps_points[0][1]),
		popup = 'Start',
		icon=folium.Icon(color='blue',icon='info-sign')
		).add_to(map)
	folium.Marker(
		location = (gps_points[len(gps_points)-1][0],gps_points[len(gps_points)-1][1]),
		popup = 'End',
		icon=folium.Icon(color='red',icon='info-sign')
		).add_to(map)
	gps_points = []
	map.save("./route.html")