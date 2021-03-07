# Based on https://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php

import sys
import socket
import threading
import time

from user import User
from model import DataModel
import display

model = DataModel()
waiting = 2
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

	sock.settimeout(2)
	sock.send(('@' + name + '$').encode())

	while running:
		# incoming message from remote server, s
		try:
			dataset = sock.recv(4096).decode()
			if not dataset:
				model.add_message('<Disconnected>')
				model.quit = True
				return

			for data in dataset.split('$'):
				if len(data) == 0:
					continue
				elif data[0] == "C":
					# print message
					if int(data.split('&')[0][1:]) == model.me.room:
						model.add_message(data.split('&')[1])
				elif data[0] == 'M':
					# move user
					data = data.split('&')
					i = int(data[0][1:])
					model.users[i].pos = int(data[1])
					model.users[i].room = int(data[2])
				elif data[0] == 'N':
					# change username
					print('That name is invalid or already taken')
					name = input('Try a different name: ')
					sock.send(('@' + name).encode())
				elif data[0] == "J":
					# add user
					user = User(data[1:])
					model.users[user.index] = user
					model.refresh()
					model.add_message("<%s Joined the server>" % user.name)
				elif data[0] == "U":
					# add existing users
					user = User(data[1:])
					model.users[user.index] = user
					if user.name == name and model.me == None:
						model.add_message(name + ' connected to server')
						model.me = user
						waiting -= 1
					model.refresh()
				elif data[0] == "L":
					# remove user
					name = model.users[int(data[1:])].name
					del model.users[int(data[1:])]
					model.refresh()
					model.add_message("<%s Left the server>" % name)
				elif data[0] == "D" and waiting:
					# load map details
					model.hall.deserialize(data)
					waiting -= 1
		except socket.timeout:
			while not model.send.empty():
				sock.send(("C%d&[%s] %s$" % (model.me.room, name, model.send.get())).encode())
			if model.moved:
				sock.send(("M%d&%d&%d$" % (model.me.index, model.me.pos, model.me.room)).encode())
	model.add_message('<Disconnected>')
	model.quit = True

if __name__ == "__main__":
	try:
		name = ''
		if(len(sys.argv) < 2):
			print('Usage : python client.py <hostname> username')
			sys.exit()
		elif(len(sys.argv) < 3):
			name = input('Enter username: ')
		else:
			name = sys.argv[2]

		start(sys.argv[1], 1234, name)
		sys.exit(0)
	except KeyboardInterrupt:
		print('\nInterrupted')
		sys.exit(0)
