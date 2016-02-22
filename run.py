#!/usr/bin/python

import argparse
import pyshark
import signal, sys
import collections

class PacketStats:
	window_size = 10

	def __init__(self, packet_type):
		self.packet_type = packet_type
		self.packets = collections.deque()
		self.total_length = 0

	def add_packet(self, packet):
		if packet.length >= 0:
			self.packets.append({'timestamp': float(packet.sniff_timestamp), 'length': float(packet.length)})
			self.total_length += float(packet.length)
			while float(float(packet.sniff_timestamp) - self.packets[0]['timestamp']) > self.window_size:
				self.total_length -= self.packets[0]['length']
				self.packets.popleft()

def signal_handler(signal, frame):
	for packet_type in packet_stats:
		print packet_type + ': ' + str(packet_stats[packet_type].total_length)
		if len(packet_stats[packet_type].packets) > 0:
			print len(packet_stats[packet_type].packets)
			print packet_stats[packet_type].packets[0]['timestamp']
			print packet_stats[packet_type].packets[-1]['timestamp']
	sys.exit(0)

##########

parser = argparse.ArgumentParser()
parser.add_argument('interface', help='interface to capture')
args = parser.parse_args()

capture = pyshark.LiveCapture(interface=args.interface)

packet_stats = {'arp': PacketStats('arp'), 'icmp': PacketStats('icmp'), 'tcp': PacketStats('tcp'), 'udp': PacketStats('udp'), 'other': PacketStats('other')}

signal.signal(signal.SIGINT, signal_handler)

for packet in capture.sniff_continuously():
	if hasattr(packet, 'tcp'):
		packet_stats['tcp'].add_packet(packet) 
	elif hasattr(packet, 'udp'):
		packet_stats['udp'].add_packet(packet) 
	elif hasattr(packet, 'arp'):
		packet_stats['arp'].add_packet(packet) 
	elif hasattr(packet, 'icmp'):
		packet_stats['icmp'].add_packet(packet) 
	else:
		packet_stats['other'].add_packet(packet) 
