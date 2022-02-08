import struct
import binascii

# Unpack Ethernet Frame
def ethernet_frame(data):
	ip_header = struct.unpack("!6s6sH", data[0:14])
	return binascii.hexlify(ip_header[0]), binascii.hexlify(ip_header[1]), ip_header[2], data[14:]

# Unpack IPv4 Packets
def ipv4_packet(data):
	version_header_len = data[0]
	version = version_header_len >> 4
	header_len = (version_header_len & 15) * 4
	ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
	return version, header_len, ttl, proto, ipv4(src), ipv4(target), data[header_len:]

# Get IP address (string)
def ipv4(addr):
	return '.'.join(map(str, addr))

# Unpack UDP packet
def udp_seg(data):
	src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
	return src_port, dest_port, size, data[8:]