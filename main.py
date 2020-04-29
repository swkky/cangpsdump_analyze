import sys
import my_module.gps_func as myGPSfunc
import my_module.data_check as myDATACHECKfunc

if __name__ == '__main__':
    if sys.argv[1] == 'show_route':
        logfile = sys.argv[2]
        myGPSfunc.show_route_from_gps(logfile)
    if sys.argv[1] == 'detect_turn':
        logfile = sys.argv[2]
        myGPSfunc.detect_turn_from_gps(logfile)
    #myDATACHECKfunc.check_time_gap(logfile)