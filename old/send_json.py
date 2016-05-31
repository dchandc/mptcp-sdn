#!/usr/bin/python

import argparse
import signal
import sys
import subprocess
import os
import json
import socket
import update_pb2

def send_json(args):
    with open(os.path.join(args.output_dir, args.json_file)) as json_file:
        json_obj = json.load(json_file)
        json_str = json.dumps(json_obj)

        update = update_pb2.Update()
        update.type = update_pb2.Update.FLOW
        update.data = json_str

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((args.address, args.port))
        s.send(update.SerializeToString())
        s.close()

def signal_handler(signal, frame):
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('address', help='destination IP address')
    parser.add_argument('port', type=int, help='destination port')
    parser.add_argument('-o', '--output-dir', default='output',
                        help='captcp output directory')
    parser.add_argument('-j', '--json-file', default='captcp.json',
                        help='captcp json file')
    args = parser.parse_args()

    send_json(args)

if __name__ == '__main__':
    main()
