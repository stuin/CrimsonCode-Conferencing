import queue
from map import Map

class DataModel(object):
	def __init__(self):
		self.send = queue.Queue()
		self.hall = Map()
		self.users = {}
		self.me = None
		self.log = []
		self.i = 0

		# boolean flags
		self.moved = False
		self.dirty = False

	def get_users(self):
		return [ (user.name, user.index) for user in self.users.values() ]

	def get_messages(self):
		return self.log

	def get_map(self):
		return self.hall.draw(self.users)

	def get_height(self):
		return len(self.hall.content)

	def add_message(self, message):
		self.log.append((message, self.i))
		self.i += 1

	def send_message(self, message):
		self.add_message("[Me] " + message)
		self.send.put(message)

	def add_move(self, direction):
		if self.me and self.hall.move(self.me, direction):
			if self.me.changed:
				self.add_message('<Moved to %s>' % self.hall.rooms[self.me.room])
				self.me.changed = False
			self.moved = True

