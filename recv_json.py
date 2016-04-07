#!/usr/bin/python

import argparse
import signal
import sys
import os
import json
import socket

def recv_json(args):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((args.address, args.port))
    s.listen(1)

    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print data
    conn.close()

def signal_handler(signal, frame):
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('address', help='bind IP address')
    parser.add_argument('port', type=int, help='bind port')
    args = parser.parse_args()

    recv_json(args)

if __name__ == '__main__':
    main()
