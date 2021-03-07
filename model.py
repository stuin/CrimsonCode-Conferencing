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
		self.userlist = []
		self.map = ''

		# boolean flags
		self.moved = False
		self.quit = False

	def refresh(self):
		user_room = []
		user_other = []
		self.map = self.hall.draw(self.users)
		if self.me:
			for user in self.users.values():
				if user == self.me:
					pass
				elif user.room == self.me.room:
					user_room.append((user.name, user.index))
				else:
					user_other.append((user.name, user.index))
			self.userlist = user_room + user_other

	def get_height(self):
		return len(self.hall.content.split('\n'))

	def add_message(self, message):
		if len(self.log) > self.log_height - 1:
			self.log = self.log[1:]
		self.log.append((message, self.i))
		self.i += 1

	def send_message(self, message):
		self.add_message("[%s] " % self.me.name + message)
		self.send.put(message + "$")

	def add_move(self, direction):
		if self.me and self.hall.move(self.me, direction):
			self.refresh()
			if self.me.changed:
				self.add_message('<Moved to %s>' % self.hall.rooms[self.me.room])
				self.me.changed = False
			self.moved = True

