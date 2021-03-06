# Based on https://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php

import sys
import socket
import select

from user import User
from map import Map

def chat_client(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	hall = None

	# connect to remote host
	try:
		s.connect((host, port))
	except:
		print('Unable to connect')
		sys.exit()

	print('Connected to remote host. You can start sending messages')
	sys.stdout.write('[Me] '); sys.stdout.flush()

	while 1:
		socket_list = [sys.stdin, s]

		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

		for sock in ready_to_read:
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096).decode()
				if not data:
					print('\nDisconnected from chat server')
					sys.exit()
				elif data[0] == "\r":
					#print data
					sys.stdout.write(data)
					sys.stdout.write('[Me] '); sys.stdout.flush()
				elif data[0] == "M" and hall == None:
					hall = Map(data[1:])
				elif data[0] == "D" and hall != None:
					hall.deserialize(data)
				else:
					print("\rSystem message\n" + data + "\n[Me] ")


			else :
				# user entered a message
				msg = sys.stdin.readline()
				s.send(str.encode(msg))
				sys.stdout.write('[Me] '); sys.stdout.flush()

if __name__ == "__main__":
	try:
		if(len(sys.argv) < 3):
			print('Usage : python client.py hostname')
			sys.exit()

		sys.exit(chat_client(sys.argv[1], 1234))
	except KeyboardInterrupt:
		print('Interrupted')
		sys.exit(0)
