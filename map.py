import ast
from enum import IntEnum

class DIRECTION(IntEnum):
	UP = -1
	DOWN = 1
	LEFT = -1
	RIGHT = 1

class Map(object):
	def __init__(self, content=None):
		self.doors = {}
		self.rooms = []
		self.blocked = ['#', '>']
		self.content = ''
		if content:
			self.read_map(content)

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
			to += dir.value * self.width

		if self.content.get(to) in blocked:
			return False

		if self.content.get(user.pos) == '-' and user.pos in self.doors:
			if to > user.pos:
				user.room = self.doors[user.pos][1]
			else:
				user.room = self.doors[user.pos][0]
			user.pos = to
			return True

		user.pos = to
		return False

	def serialize(self):
		return ('D' + str(self.doors) + '$' + str(self.rooms) + '$' + self.content).encode()

	def deserialize(self, data):
		data = data[1:].split('$')
		self.doors = ast.literal_eval(data[0])
		self.rooms = list(data[1])
		self.read_map(data[2])

	def read_map(self, content):
		self.width = max([ len(s) for s in content ])
		content = [(x + ' ' * (self.width - len(x))) for x in content]
		self.content = ''.join(content)
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
		self.add_door(30, 14, 3, 4)
		self.add_door(30, 10, 3, 5)
		self.add_door(30,  6, 3, 6)




