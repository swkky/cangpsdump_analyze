# -+- coding: utf-8 -*-
import sys
import numpy as np
import gpxpy
import folium
import datetime
import matplotlib.pyplot as plt
import my_module.log_format as lf
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


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

###########################################
#ログデータから緯度，経度(同一データ無し)のみを取り出して経路をhtmlで出力
###########################################
def show_route_from_gps(args):
    #if start gps fix fix_flag turns 1
    fix_flag = 0
    previous_gps_count = -1
    #gps_points[[latitude],[longitude]]
    gps_points = []
    gps_counts = []
    #process for log file
    file_path = args.file_path
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
                gps_counts.append(gps_count)
                #print(gps_count,latitude,longitude,gps_speed,gps_track)
                gps_points.append([latitude,longitude])
    #################################################
    # create map process
    #################################################
    #print(gps_points)
    map = folium.Map(location=[gps_points[0][0],gps_points[0][1]], zoom_start=20)
    # add map tiling options
    folium.TileLayer('Mapbox Bright').add_to(map)
    folium.TileLayer('cartodbdark_matter').add_to(map)
    folium.TileLayer('openstreetmap').add_to(map)
    folium.LayerControl().add_to(map)
    #経路をプロット
    folium.PolyLine(locations = gps_points).add_to(map)
    #全ての地点にマーカーを置く
    for i in range(len(gps_points)):
        folium.Marker(
            location = (gps_points[i][0],gps_points[i][1]),
            popup = i
        ).add_to(map)
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
    output = "./" + file_path.rstrip(".log") + "_route_plot_all.html"
    map.save(output)


###########################################
#右折，左折を検出したい########################
###########################################
def detect_turn_from_gps(args):
    #if start gps fix fix_flag turns 1
    fix_flag = 0
    #合計走行距離
    mileage = 0
    previous_gps_count = -1
    #gps_points[[latitude],[longitude],[can_receive_time]]
    gps_points = []
    only_latlong = []
    #from logging data
    gps_speeds = []
    #calculated speed
    speed_array = np.array([])
    track_array = np.array([])
    receive_time_array = np.array([])
    #process for log file
    file_path = args.file_path
    logfile = open(file_path, 'r')
    for line in logfile:
        line_spt = line.split()
        #print(len(line_spt))
        #end of file
        if len(line_spt) < 3:
            break
        if len(line_spt) == lf.row_num:
            fix_status = int(line_spt[lf.row_gps_mode])
            can_receive_time = float(line_spt[lf.row_can_receive_time])
            gps_fix_time = float(line_spt[lf.row_gps_fix_time])
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
                #print(gps_fix_time,gps_count,latitude,longitude,gps_speed,gps_track)
                gps_points.append([latitude,longitude,gps_fix_time])
                only_latlong.append([latitude,longitude])
                track_array = np.append(track_array,gps_track)
                gps_speeds.append(gps_speed)
                #総走行距離算出，時速，
                if len(gps_points) >= 2:
                    distance = cal_distance(gps_points[len(gps_points)-2][0], gps_points[len(gps_points)-2][1], gps_points[len(gps_points)-1][0], gps_points[len(gps_points)-1][1])
                    time_diff = gps_points[len(gps_points)-1][2] - gps_points[len(gps_points)-2][2]
                    mileage += distance
                    speed_m_sec = (distance * 1000) / time_diff
                    speed_array = np.append(speed_array,speed_m_sec)
                    #Unix timeをdatetime型に変換(日付，時刻)
                    receive_datetime = (datetime.datetime.fromtimestamp(can_receive_time))
                    #datetime型の時刻部分のみに(.time)
                    #receive_datetime = datetime.datetime.time(receive_datetime)
                    receive_time_array = np.append(receive_time_array,receive_datetime)
                    if args.debug:
                        print(len(gps_speeds))
                        print("dist  :",distance)
                        print("time  :",time_diff)
                        print("speed:",speed_m_sec,"[m/sec]",'\n')
    print(file_path)
    print("直線距離",cal_distance(gps_points[0][0],gps_points[0][1],gps_points[len(gps_points)-1][0],gps_points[len(gps_points)-1][1]),"[km]")
    print("走行距離",mileage,"[km]")
    print((receive_time_array[len(receive_time_array)-1] - receive_time_array[0]).seconds)
    print("Fix Hz",(gps_count - 4) / (receive_time_array[len(receive_time_array)-1] - receive_time_array[0]).seconds,"[Hz]",'\n')
    
    if args.range is not None:
        plot_start = args.range[0]
        plot_end = args.range[1]
        #################################################
        # create speed(2 type) and track graph
        #################################################
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ln1=ax1.plot(receive_time_array[plot_start:plot_end],speed_array[plot_start:plot_end],'C0',label=r'speed',marker="o")

        ax2 = ax1.twinx()
        ln2=ax2.plot(receive_time_array[plot_start:plot_end],track_array[plot_start:plot_end],'C1',label=r'track',marker="o")

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc='upper right')

        ax1.set_xlabel('time')
        ax1.set_ylabel(r'speed[m/sec]')
        ax2.set_ylabel(r'track[degree]')
        ax2.set_yticks([0,90,180,270,360])
        ax2.grid(True)
        plt.show()
        ######################################################
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ln1=ax1.plot(receive_time_array[plot_start:plot_end],gps_speeds[plot_start:plot_end],'C0',label=r'speed',marker="o")

        ax2 = ax1.twinx()
        ln2=ax2.plot(receive_time_array[plot_start:plot_end],track_array[plot_start:plot_end],'C1',label=r'track',marker="o")

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc='upper right')

        ax1.set_xlabel('time')
        ax1.set_ylabel(r'speed from GPS[m/sec]')
        ax1.grid(True)
        ax2.set_ylabel(r'track[degree]')
        ax2.set_ylim([0,360])
        plt.show()
    #################################################
    # create map process
    #################################################
    #print(only_latlong)
    map = folium.Map(location=[only_latlong[0][0],only_latlong[0][1]], zoom_start=20)
    # add map tiling options
    folium.TileLayer('Mapbox Bright').add_to(map)
    folium.TileLayer('cartodbdark_matter').add_to(map)
    folium.TileLayer('openstreetmap').add_to(map)
    folium.LayerControl().add_to(map)
    #指定された範囲の経路をhtmlで出力
    if args.range is not None:
        folium.PolyLine(locations = only_latlong[plot_start:plot_end]).add_to(map)
        #create Icon of start(blue) and end(red)
        folium.Marker(
            location= (only_latlong[plot_start][0],only_latlong[plot_start][1]),
            popup = plot_start,
            icon=folium.Icon(color='blue',icon='info-sign')
            ).add_to(map)
        folium.Marker(
            location = (only_latlong[plot_end][0],only_latlong[plot_end][1]),
            popup = plot_end,
            icon=folium.Icon(color='red',icon='info-sign')
            ).add_to(map)
        only_latlong = []
        output = "./" + file_path.rstrip(".log") + "_" + str(plot_start) + "_" + str(plot_end) + "_plot.html"
        map.save(output)
    #全ての経路をhtmlファイルで出力
    else:
        folium.PolyLine(locations = only_latlong).add_to(map)
        #create Icon of start(blue) and end(red)
        folium.Marker(
            location= (only_latlong[0][0],only_latlong[0][1]),
            popup = 'start',
            icon=folium.Icon(color='blue',icon='info-sign')
            ).add_to(map)
        folium.Marker(
            location = (only_latlong[len(only_latlong)-1][0],only_latlong[len(only_latlong)-1][1]),
            popup = 'end',
            icon=folium.Icon(color='red',icon='info-sign')
            ).add_to(map)
        only_latlong = []
        output = "./" + file_path.rstrip(".log") + "_plot_all.html"
        map.save(output)



#２地点(a,b)の緯度経度情報から距離を計算する（km）
def cal_distance(lat_a,lon_a,lat_b,lon_b):
    if lat_a == lat_b and lon_a == lon_b:
        distance = 0
    else:
        ra=6378.140  # equatorial radius (km)
        rb=6356.755  # polar radius (km)
        F=(ra-rb)/ra # flattening of the earth
        rad_lat_a=np.radians(lat_a)
        rad_lon_a=np.radians(lon_a)
        rad_lat_b=np.radians(lat_b)
        rad_lon_b=np.radians(lon_b)
        pa=np.arctan(rb/ra*np.tan(rad_lat_a))
        pb=np.arctan(rb/ra*np.tan(rad_lat_b))
        xx=np.arccos(np.sin(pa)*np.sin(pb)+np.cos(pa)*np.cos(pb)*np.cos(rad_lon_a-rad_lon_b))
        c1=(np.sin(xx)-xx)*(np.sin(pa)+np.sin(pb))**2/np.cos(xx/2)**2
        c2=(np.sin(xx)+xx)*(np.sin(pa)-np.sin(pb))**2/np.sin(xx/2)**2
        dr=F/8*(c1-c2)
        distance=ra*(xx+dr)
    return distance