import sys
import argparse
import my_module.gps_func as myGPSfunc
import my_module.data_check as myDATACHECKfunc

def main(command_line=None):
    parser = argparse.ArgumentParser(
        usage='can and GPS data analyze tools',
        add_help=True,
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug info'
    )
    subprasers = parser.add_subparsers(dest='command')

    show_route = subprasers.add_parser('show_route', help='show route people')
    show_route.add_argument('file_path', help='file_path to show_route')

    detect_turn = subprasers.add_parser('detect_turn', help='detect_turn')
    detect_turn.add_argument('file_path', help='file_path to detect_turn')
    #引数を解析する
    args = parser.parse_args(command_line)
    if args.debug:
        print("debug: " + str(args))
    if args.command == 'show_route':
        myGPSfunc.show_route_from_gps(args)
    if args.command == 'detect_turn':
        myGPSfunc.detect_turn_from_gps(args)

if __name__ == '__main__':
    main()