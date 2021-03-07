# Based on https://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php

import sys
import socket
import select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 1234

from user import User
from map import Map

def run_server():
	# set up server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)
	SOCKET_LIST.append(server_socket)

	# set up meeting hall
	mapfile=open("map.txt", "r")
	mapdata=mapfile.readlines()
	hall = Map(mapdata)
	hall.setup_1()

	# prepare list for users
	all_users = {}
	room = []
	for r in hall.rooms:
		room.append([])

	print("Server started on port", PORT)

	while 1:
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

		for sock in ready_to_read:
			# a new connection request recieved
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				print("Client (%s, %s) connected" % addr)
				sockfd.send(("M" + hall.content).encode())
				sockfd.send(hall.serialize())

			# a message from a client, not a new connection
			else:
				# process data recieved from client,
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER).decode()
					if data and addr in all_users:
						# there is something in the socket
						broadcast(server_socket, sock, room[all_users[addr].room], "\r[%s] " % all_users[addr].name + data)
					elif data:
						# add user
						user = User(data[1:], hall.startPos)
						user.socket = sockfd
						all_users[addr] = user
						room[0].append(user)

						print("Client (%s, %s) set name to" % addr, data)
						broadcast(server_socket, sockfd, room[0], "J" + user.serialize())
					else:
						# remove the socket that's broken
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)

						# remove user from lists
						user = all_users[addr]
						room[user.room].remove(user)
						del all_users[addr]

						print("\rClient @%s Lost connection" % user.name)
						broadcast(server_socket, room[user.room], "L" + user.name)

				# exception
				except:
					if addr in all_users:
						# remove user from lists
						user = all_users[addr]
						room[user.room].remove(user)
						del all_users[addr]

						print("\rClient @%s Lost connection" % user.name)
						broadcast(server_socket, sock, room[all_users[addr].room], "L" + all_users[addr].name)
					else:
						print("\rClient (%s, %s) Lost connection" % addr)
					continue

	server_socket.close()

# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, room, message):
	for user in room:
		socket = user.socket
		# send the message only to peer
		if user.socket != sock:
			try:
				socket.send(str.encode(message))
			except:
				# broken socket connection
				socket.close()
				# broken socket, remove it
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)

if __name__ == "__main__":
	try:
		sys.exit(run_server())
	except KeyboardInterrupt:
		print('\nInterrupted')
		sys.exit(0)
