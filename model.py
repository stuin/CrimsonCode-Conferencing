import queue
from map import Map

class DataModel(object):
	def __init__(self):
		self.send = queue.Queue()
		self.hall = Map()
		self.users = {}
		self.me = None
		self.i = 0
		self.log_height = 100

		# directly accessed lists
		self.log = []
		self.user_list = []
		self.map = ''
		self.room = ''
		self.pinned = ''

		# boolean flags
		self.moved = False
		self.help = False
		self.quit = False

	def refresh(self):
		user_room = []
		user_other = []
		if not self.help:
			self.map = self.hall.draw(self.users)

		# list users
		if self.me:
			r = self.me.room
			self.room = self.hall.rooms[r] + ": " + self.hall.pinned[r]
			for user in self.users.values():
				if user == self.me:
					pass
				elif user.room == self.me.room:
					user_room.append((user.name, user.index))
				else:
					user_other.append((user.name, user.index))
			self.user_list = user_room + user_other

	def get_height(self):
		return len(self.hall.content.split('\n'))

	def add_message(self, message):
		if len(self.log) > self.log_height - 2:
			self.log = self.log[1:]
		self.log.append((message, self.i))
		self.i += 1

	def send_message(self, message):
		self.add_message("[%s] " % self.me.name + message)
		self.send.put("C%d&[%s] %s\n$" % (self.me.room, self.me.name, message))

	def add_move(self, direction):
		self.help = False
		if self.me and self.hall.move(self.me, direction):
			if self.me.changed:
				self.add_message('<Moved to %s>' % self.hall.rooms[self.me.room])
				self.me.changed = False
			self.moved = True

