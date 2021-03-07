# Based on https://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php

import sys
import socket
import select
import threading
import time

from user import User
from map import Map
import display

hall = Map()
all_users = {}
waiting = True

def run_client(host, port, name):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	me = None
	global hall
	global all_users
	global waiting

	# connect to remote host
	try:
		s.connect((host, port))
	except:
		print('Unable to connect')
		sys.exit()

	print(name + ' connected to server')
	s.send(('@' + name).encode())
	sys.stdout.write('[Me] '); sys.stdout.flush()

	while 1:
		socket_list = [s]

		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

		for sock in ready_to_read:
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096).decode()
				print(data[0])
				if not data:
					print('\nDisconnected from chat server')
					sys.exit()
				elif data[0] == "\r":
					# print message
					sys.stdout.write(data)
					sys.stdout.write('[Me] '); sys.stdout.flush()
				elif data[0] == "J":
					# add user
					user = User(data[1:])
					all_users[user.name] = user
					print("\r<%s Entered the room>" % user.name)
					sys.stdout.write('[Me] '); sys.stdout.flush()
				elif data[0] == "L":
					# remove user
					del all_users[data[1:]]
					print("\r<%s Left the room>" % data[1:])
					sys.stdout.write('[Me] '); sys.stdout.flush()
				elif data[0] == "D" and me == None:
					# load map details
					hall.deserialize(data)
					me = User(name, hall.startPos)
					all_users[name] = me
					waiting = False
				else:
					print("\rSystem message\n" + data)
			else:
				# user entered a message
				msg = sys.stdin.readline()
				s.send(msg.encode())
				sys.stdout.write('[Me] '); sys.stdout.flush()

if __name__ == "__main__":
	try:
		if(len(sys.argv) < 3):
			print('Usage : python client.py hostname username')
			sys.exit()

		#name = input('Enter username: ')

		t1=threading.Thread(target=run_client, args=(sys.argv[1], 1234, sys.argv[2]))
		t1.start()
		while waiting:
			time.sleep(1)
			print("Start display")
		display.start_display(hall, all_users)
		sys.exit()
	except KeyboardInterrupt:
		print('\nInterrupted')
		sys.exit(0)
