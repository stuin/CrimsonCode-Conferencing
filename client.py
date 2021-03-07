# Based on https://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php

import sys
import socket
import threading
import time

from user import User
from model import DataModel
import display

model = DataModel()
waiting = True
running = True

def start(host, port, name):
	t1=threading.Thread(target=run_client, args=(host, port, name))
	t1.start()
	while waiting:
		time.sleep(1)

	print("Connected")
	display.start_display(model)

	global running
	running = False
	return

def run_client(host, port, name):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(2)

	global model
	global waiting

	# connect to remote host
	try:
		sock.connect((host, port))
	except:
		print('Unable to connect')
		sys.exit()

	model.add_message(name + ' connected to server')
	sock.settimeout(2)
	sock.send(('@' + name).encode())

	while running:
		# incoming message from remote server, s
		try:
			data = sock.recv(4096).decode()
			if not data:
				model.add_message('<Disconnected from server>')
				return
			if data[0] == "[":
				# print message
				model.add_message(data)
			elif data[0] == "U":
				for u in data.split("U"):
					if len(u) > 0:
						# add user
						user = User(u)
						model.users[user.index] = user
			elif data[0] == "J":
				user = User(data[1:])
				model.users[user.index] = user
				model.add_message("<%s Entered the room>" % user.name)
			elif data[0] == "L":
				# remove user
				del model.users[data[1:]]
				model.add_message("<%s Left the room>" % data[1:])
			elif data[0] == "D" and waiting:
				# load map details
				model.hall.deserialize(data)
				waiting = False
		except socket.timeout:
			while not model.send.empty():
				sock.send(("[%s] " % name + model.send.get()).encode())

if __name__ == "__main__":
	try:
		if(len(sys.argv) < 3):
			print('Usage : python client.py hostname username')
			sys.exit()

		#name = input('Enter username: ')
		start(sys.argv[1], 1234, sys.argv[2])
		sys.exit(0)
	except KeyboardInterrupt:
		print('\nInterrupted')
		sys.exit(0)
