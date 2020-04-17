import sys
import my_module.gps_func as myGPSfunc
import my_module.data_check as myDATACHECKfunc

if __name__ == '__main__':
    logfile = sys.argv[1]
    myGPSfunc.show_route_from_gps(logfile)
    #myDATACHECKfunc.check_time_gap(logfile)