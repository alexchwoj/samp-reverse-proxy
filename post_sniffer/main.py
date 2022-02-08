# Lib
import socket
from wsgiref.validate import validator
import requests

# Modules
import sys
sys.path.append('../')

from utils.samp_datagram import unKyretardizeDatagram
from utils.unpack_head import *

# Config
validator_url = 'http://loadbalancer.samp.valider.hyaxe.com:60422'
validator_key = 'Y$Lga#5p@ZPG8fex4rNVwuEQSFsvTRnWM+Hbm2KUByJk93tq7D'

# Register
shared_validated = []
public_address = requests.get('https://api.ipify.org').text

def main():
	conn = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
	print(f'Hyaxe - Post Sniffer\nSocket object: {conn}\nPublic address: {public_address}\n')
 
	while True:
		raw_data, addr = conn.recvfrom(65536)
		dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)

		# IPv4 (2048)
		if eth_proto == 2048:
			(version, header_length, ttl, proto, src, target, data) = ipv4_packet(data)

			# UDP (17)
			if proto == 17:
				try:
					src_port, dest_port, length, data = udp_seg(data)
				except:
					continue

				# Ignore queries
				if data[:4] == b'SAMP':
					continue

				# Get int list
				values = unKyretardizeDatagram(data, dest_port)
				if not values:
					continue

				conn_address = f'{src}:{src_port}'
				
				if len(values) == 47:
					if not conn_address in shared_validated:
						print(F"[Client join] Registered proxy in port {dest_port} > {conn_address} (len: {len(values)})")
						shared_validated.append(conn_address)

						# Validate
						payload = ""
						for value in values:
							payload += str(value)
							
						try:
							req = requests.post(
								f'{validator_url}/proxy/register/proxied_player',
								headers = {
									'Authorization': validator_key
								},
								json = {
									'address': conn_address,
									'payload': payload
								},
								timeout = 4
							)
							print(f'[Validator] Validated proxy {conn_address}, response: {req.json()}')
						except Exception as e:
							print(f'[Error in validation] {e}')

# Start listening
main()