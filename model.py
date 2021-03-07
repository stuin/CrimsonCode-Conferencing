import queue
from map import Map

class DataModel(object):
	def __init__(self):
		self.send = queue.Queue()
		self.hall = Map()
		self.users = {}
		self.log = []
		self.i = 0

	def copy(self, other):
		self.hall = other.hall
		self.users = other.users
		self.log = other.log

	def get_users(self):
		return [ (user.name, user.index) for user in self.users.values() ]

	def get_messages(self):
		return self.log

	def get_map(self):
		return self.hall.content

	def get_height(self):
		return len(self.hall.content)

	def add_message(self, message):
		self.log.append((message, self.i))
		self.i += 1

	def send_message(self, message):
		self.add_message("[Me] " + message)
		self.send.put(message)

