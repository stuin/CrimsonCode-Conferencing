import ast
from enum import IntEnum

class DIRECTION(IntEnum):
	UP = -2
	DOWN = 2
	LEFT = -1
	RIGHT = 1

class Map(object):
	def __init__(self, content=None):
		self.doors = {}
		self.rooms = []
		self.blocked = ['#', '>']
		self.content = ''
		if content:
			self.width = max([ len(s) for s in content ])
			content = [(x + ' ' * (self.width - len(x))) for x in content]
			self.content = ''.join(content)
			self.startPos = self.content.find('>') + 1

	def pos(self, x, y):
		return (y * self.width + x)

	def add_door(self, x, y, side1, side2):
		p = self.pos(x-1, y-1)
		if(self.content[p] == '-'):
			self.doors[p] = (side1, side2)
		else:
			print("No door at (%d, %d) %c" % (x-1, y-1, self.content[0]))

	def move(self, user, dir):
		to = user.pos
		if dir == DIRECTION.LEFT or dir == DIRECTION.RIGHT:
			to += dir.value
		else:
			to += int(dir.value / 2 * self.width)

		if self.content[to] in self.blocked:
			return False

		if self.content[user.pos] == '-' and user.pos in self.doors:
			r = user.room
			if to < user.pos:
				user.room = self.doors[user.pos][1]
			else:
				user.room = self.doors[user.pos][0]
			if user.room != r:
				user.changed = 2
			user.pos = to
			return True

		user.pos = to
		return True

	def draw(self, users):
		output = self.content
		for u in users.values():
			output = output[:u.pos] + u.avatar[0] + output[u.pos + 1:]
		return output

	def serialize(self):
		return ('D' + str(self.doors) + '&' + str(self.rooms) + '&' + self.content + "$").encode()

	def deserialize(self, data):
		data = data[1:].split('&')
		self.doors = ast.literal_eval(data[0])
		self.rooms = ast.literal_eval(data[1])
		self.width = data[2].find('\n') + 1
		self.content = data[2]
		self.startPos = self.content.find('>') + 1

	# default map setup
	def setup_1(self):
		self.rooms = [
			'Entrance Hall', 'Main Theatre', 'Side Theatre',
			'Side Hallway', 'Room 1', 'Room 2', 'Room 3']

		# large doors
		for x in range (13, 16):
			self.add_door(x, 11, 0, 1)
		for x in range (20, 23):
			self.add_door(x, 16, 0, 2)
		for x in range (27, 30):
			self.add_door(x, 16, 0, 3)

		# side rooms
		self.add_door(30, 14, 4, 3)
		self.add_door(30, 10, 5, 3)
		self.add_door(30,  6, 6, 3)




